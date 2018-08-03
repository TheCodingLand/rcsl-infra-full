module.exports = (app) => {
    const multer = require('multer');
    const storage = multer.diskStorage({
      destination: app.get('destination'),
      filename: function (req, file, cb) {
        let ext=""
        // Mimetype stores the file type, set extensions according to filetype
        switch (file.mimetype) {
          case 'application/pdf':
            ext = '.pdf';
            break;
          case 'image/jpg':
            ext = '.jpg';
            break;          
        }
  
        cb(null, file.originalname.slice(0, -4) + ext);
      }
    });
    const upload = multer({storage: storage});
    
    


    app.post('/uploadHandler', upload.single('file'), function (req, res, next) {
      if (req.file && req.file.originalname) {
        console.log(`Received file ${req.file.originalname}`);
      }
  
      res.send({ responseText: req.file.path }); // You can send any response to the user here
    });
    app.post('/getstatus', function (req, res, next) {
        if (req.file && req.file.originalname) {
          console.log(`Received file ${req.file.originalname}`);
        }
    
        res.send({ responseText: "file conversion in progress :" + req.file.path }); // You can send any response to the user here
      });

    
  }