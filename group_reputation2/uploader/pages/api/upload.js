import fs from 'fs';
import formidable from 'formidable';

export const config = {
  api: {
    bodyParser: false,
    externalResolver: true,
  },
};

export default async (req, res) => {
  if (fs.existsSync('userdata.csv')) {
    try {
      fs.unlinkSync('userdata.csv');
    } catch (err) {
      res.status(500).send(err.message);
    }
  }

  const form = new formidable.IncomingForm();
  form.uploadDir = './';
  form.keepExtensions = true;

  form.parse(req, (err, fields, files) => {
    if (err) return res.status(500).send(err.message);

    fs.rename(files.file.path, 'userdata.csv', err2 => {
      if (err2) return res.status(500).send(err2.message);
      res.status(200).end();
    });
  });
  
}
