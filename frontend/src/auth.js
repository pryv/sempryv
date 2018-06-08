import pryv from "pryv";

export default {
  isConnected(callback, error) {
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
    localStorage.setItem("domain", domain);
    localStorage.setItem("username", username);
    localStorage.setItem("token", token);
  },
  logout() {
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
    return new pryv.Connection({
      domain: localStorage.domain,
      username: localStorage.username,
      auth: localStorage.token
    });
  },
  pryvCredentials() {
    return {
      domain: pryv.Auth.connection.domain,
      username: pryv.Auth.connection.username,
      token: pryv.Auth.connection.auth
    };
  }
};
