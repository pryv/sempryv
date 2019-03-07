import pryv from "pryv";

export default {
  isConnected(callback, error) {
    // Check is the stored credentials offers a valid connections
    var conn = this.connection();
    conn.accessInfo(function(err) {
      if (err) {
        error();
      } else {
        callback();
      }
    });
  },
  signIn() {
    pryv.Auth.popupLogin();
  },
  signOut() {
    pryv.Auth.logout();
  },
  login(domain, username, token) {
    // Login in SemPryv by storing credentials in localstorage
    localStorage.setItem("domain", domain);
    localStorage.setItem("username", username);
    localStorage.setItem("token", token);
  },
  logout() {
    // Logout of SemPryv by removing credentials from localstorage
    localStorage.removeItem("username");
    localStorage.removeItem("token");
  },
  pryvSetup(domain, callback, error) {
    var pryvDomain = domain;
    var requestedPermissions = [
      {
        streamId: "*",
        level: "manage"
      }
    ];

    var settings = {
      requestingAppId: "sempryv",
      requestedPermissions: requestedPermissions,
      callbacks: {
        signedIn: function(authData) {
          callback(authData);
        },
        needSignin: function() {
          error();
        }
      }
    };

    pryv.Auth.config.registerURL.host = "reg." + pryvDomain;
    pryv.Auth.setup(settings);
  },
  connection() {
    // Return a new Pryv connection that can be user for requests
    return new pryv.Connection({
      domain: localStorage.domain,
      username: localStorage.username,
      auth: localStorage.token
    });
  },
  pryvCredentials() {
    // Return credentials obtainde through Pryv popup login
    return {
      domain: pryv.Auth.connection.domain,
      username: pryv.Auth.connection.username,
      token: pryv.Auth.connection.auth
    };
  }
};
