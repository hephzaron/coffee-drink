export const environment = {
  production: true,
  apiServerUrl: 'https://hephzy-coffee.herokuapp.com', // the running FLASK api server url
  auth0: {
    url: 'coffee-hephzy.us', // the auth0 domain prefix
    audience: 'drink', // the audience set for the auth0 app
    clientId: 'LyhQDSV5baiVh15yeD6hvNaEDX2svuWd', // the client id generated for the auth0 app
    callbackURL: 'https://hephzy-coffee.herokuapp.com', // the base url of the running ionic application.
    redirect_uri: 'https://hephzy-coffee.herokuapp.com'
  }
};
