import fs from 'fs';
import formidable from 'formidable';

import withSession from '../../lib/session';

export const config = {
  api: {
    bodyParser: false,
    externalResolver: true,
  },
};

export default withSession(async (req, res) => {
  const user = req.session.get('user');

  if (!user) return res.status(401).end();

  if (fs.existsSync('userdata.csv')) {
    try {
      fs.unlinkSync('userdata.csv');
    } catch (err) {
      return res.status(500).send(err.message);
    }
  }

  const form = new formidable.IncomingForm();
  form.uploadDir = './';
  form.keepExtensions = true;

  form.parse(req, (err, fields, files) => {
    if (err) return res.status(500).send(err.message);

    const { file } = files;
    if (!file) return res.status(400).send('File was not provided');

    fs.rename(file.path, 'userdata.csv', err2 => {
      if (err2) return res.status(500).send(err2.message);
      res.status(200).end();
    });
  });
});
