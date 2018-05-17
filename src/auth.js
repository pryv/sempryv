import pryv from "pryv";

export default {
  isConnected(callback, error) {
    var conn = new pryv.Connection({
      username: localStorage.username,
      auth: localStorage.token
    });

    conn.accessInfo(function(err) {
      if (err) {
        error();
      } else {
        callback();
      }
    });
  },
  login(username, token) {
    localStorage.setItem("username", username);
    localStorage.setItem("token", token);
  },
  logout() {
    localStorage.removeItem("username");
    localStorage.removeItem("token");
  },
  pryvSetup() {
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
      spanButtonID: "pryv-button",
      callbacks: {}
    };

    pryv.Auth.config.registerURL.host = "reg." + pryvDomain;
    pryv.Auth.setup(settings);
  },
  pryvCredentials() {
    return {
      username: pryv.Auth.connection.username,
      token: pryv.Auth.connection.auth
    };
  }
};
