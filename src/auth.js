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
  login(username, token) {
    localStorage.setItem("username", username);
    localStorage.setItem("token", token);
  },
  logout() {
    localStorage.removeItem("username");
    localStorage.removeItem("token");
  },
  pryvSetup(callback, error) {
    var pryvDomain = "pryv.me";
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
      username: localStorage.username,
      auth: localStorage.token
    });
  },
  pryvCredentials() {
    return {
      username: pryv.Auth.connection.username,
      token: pryv.Auth.connection.auth
    };
  }
};
