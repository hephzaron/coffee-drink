export const environment = {
  production: true,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'hephzy-coffee.us', // the auth0 domain prefix
    audience: 'drink', // the audience set for the auth0 app
    clientId: 'LA14RRAyNWjPGAqs1UpRTj7lcUhZ93qp', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
