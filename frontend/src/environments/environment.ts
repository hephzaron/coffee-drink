/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */
const dotEnv = require('dotenv');

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: process.env.AUTH0_DOMAIN_PREFIX, // the auth0 domain prefix
    audience: '', // the audience set for the auth0 app
    clientId: process.env.AUTH0_CLIENT_ID, // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
