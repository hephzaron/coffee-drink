/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: true,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-hephzy.us.auth0.com', // the auth0 domain prefix
    audience: 'drink', // the audience set for the auth0 app
    clientId: 'LyhQDSV5baiVh15yeD6hvNaEDX2svuWd', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:5000', // the base url of the running ionic application.
  }
};
