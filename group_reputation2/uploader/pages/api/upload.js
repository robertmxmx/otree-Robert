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

// TODO: Validation
function stripContents(data) {
  var result = data;
  
  // Remove header rows
  result.splice(0, 2);

  // Strip unnesecary values
  result = result.map((e, index) => {
    try {
      return {
        birth_region:   parseInt(e['Q4']),
        other_br:       e['Q4_15_TEXT'],
        pi_q1:          parseInt(e['Q6']),
        pi_q2:          parseInt(e['Q8']),
        pi_q3:          parseInt(e['Q9']),
        pi_q4:          parseInt(e['Q10']),
        pi_q5:          parseInt(e['Q11']),
        pi_q6:          parseInt(e['Q12']),
        pi_q7:          parseInt(e['Q13']),
        pay_id:         e['Q14']
      }
    } catch {
      throw new Error(`Error at row ${index+1}: Value expected to be an integer`)
    }
  });

  // Filter incorrect values
  result = result.filter(e => {
    // Make sure birth region is between 1 and 15
    if (isNaN(e.birth_region) ||
      ((e.birth_region < 1) || (e.birth_region > 15)) ||
      (e.birth_region == 15 && !e.other_br)) {
      return false;
    }

    // Make sure each pi question is between 1 and 7
    const pi_labels = ['pi_q1', 'pi_q2', 'pi_q3', 'pi_q4', 
      'pi_q5', 'pi_q6', 'pi_q7'];

    for (const p of pi_labels) {
      if (isNaN(e[p]) || (e[p] <  1) || (e[p] > 7)) return false;
    }

    // Make sure pay_id is given
    if (!e.pay_id) return false;

    return true;
  });
  
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
