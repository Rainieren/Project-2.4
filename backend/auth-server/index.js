// THIS NODEJS SERVER IS FOR TESTING PURPOSES 
// TO RUN THE SERVER , 'node index.js'  IN TERMINAL

const _ = require('lodash');
const express = require('express');
const cors = require('cors')
const fs = require('fs'); 
const app = express();
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const expressJwt = require('express-jwt');

var users = [
    { 'id': 1, 'username': 'counter', 'password': 'counter', 'function': 'counter' },
    { 'id': 2, 'username': 'keuken', 'password': 'keuken', 'function': 'keuken' },
    { 'id': 3, 'username': 'serveerder', 'password': 'serveerder', 'function': 'serveerder' }
];

const privateKey = fs.readFileSync('./private.pem', 'utf8');
const publicKey = fs.readFileSync('./public.pem', 'utf8');

const checkIfAuthenticated = expressJwt({
  secret: publicKey
});

const signOptions = {
  expiresIn: "30d",
  algorithm: 'ES256'
};

app.use(cors())

app.use(bodyParser.json());
//app.use(expressJwt({secret: privateKey}).unless({path: ['/api/auth']}));

app.get('/api', (req, res) => {
  res.json( {message: 'node.js server works...'} )
});

app.post('/api/auth', function(req, res) {
    const body = req.body;

    const user = users.find(user => user.username == body.username);
    if(!user || body.password != user.password) return res.sendStatus(401);
    
    let payload = { name: user.username, id: user.id };
    let token = jwt.sign(payload, privateKey, signOptions);
    res.json({
      message: 'ok',
      token: token,
      expiresIn: jwt.decode(token).exp
    });

    //Causes error: [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client
    //res.send({token});
});

/*
app.get('/api/secret', checkIfAuthenticated, function (req, res) {
  res.json({ message: "Success! You can not see this without a token" });
  console.log("GELUKT");
});

app.route('/api/secret')
  .get(checkIfAuthenticated, function (req, res) {
    res.json({ message: "Success! You can not see this without a token" });
  });
*/

const PORT = process.env.PORT || 4000;

app.listen(PORT, function () {
  console.log("Express starting listening on port "+PORT)
  console.log("Express running")
});