import fs from 'fs';
import formidable from 'formidable';
import * as csv from 'fast-csv';

import withSession from '../../lib/session';

export const config = {
  api: {
    bodyParser: false,
    externalResolver: true,
  },
};

// TODO: Validation for null values
function stripContents(data) {
  var result = data;
  
  result.splice(0, 2);
  result = result.map(elem => ({
    birth_region:   parseInt(elem['Q4']),
    other_br:       elem['Q4_15_TEXT'],
    pi_q1:          parseInt(elem['Q6']),
    pi_q2:          parseInt(elem['Q8']),
    pi_q3:          parseInt(elem['Q9']),
    pi_q4:          parseInt(elem['Q10']),
    pi_q5:          parseInt(elem['Q11']),
    pi_q6:          parseInt(elem['Q12']),
    pi_q7:          parseInt(elem['Q13']),
    pay_id:         elem['Q14']
  }));
  
  return {
    headers: result[0] ? Object.keys(result[0]) : [],
    rows: result
  };
}

function validateFile(filepath) {
  return new Promise((resolve, reject) => {
    const readStream = fs.createReadStream(filepath);
    
    readStream.on('error', reject);
    
    readStream.on('open', function() {
      var userdata = [];
      readStream.pipe(csv.parse({ headers: true }))
        .on('error', reject)
        .on('data', data => userdata.push(data))
        .on('end', () => {
          var data;
          try {
            data = stripContents(userdata);
          } catch (err) {
            reject(err);
          }
          resolve(data)
        });
    });
  });
}

export default withSession(async (req, res) => {
  const user = req.session.get('user');
  
  if (!user) return res.status(401).end();
  
  const form = new formidable.IncomingForm();
  form.uploadDir = './';
  form.keepExtensions = true;
  
  form.parse(req, async (err, fields, files) => {
    if (err) return res.status(500).send(err.message);
    
    // Check if file was even given
    const { file } = files;
    if (!file) return res.status(400).send('File was not provided');
    
    var data;
    
    // Check that file contents are valid
    try {
      data = await validateFile(file.path)
    } catch (err2) {
      return res.status(500).send(err2.message);
    }
    
    // Remove old file
    fs.unlink(file.path, () => {});

    // Write to file
    fs.writeFile('userdata.json', JSON.stringify(data), function(err2) {
      if (err2) return res.status(500).send(err.message);
      res.status(200).end();
    });
  });
});
