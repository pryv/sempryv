import pryv from "pryv";

// export function connect() {
//   var credentials = null;
//   var pryvDomain = "pryv.me";
//   var requestedPermissions = [
//     {
//       streamId: "*",
//       level: "manage"
//     }
//   ];

//   var settings = {
//     requestingAppId: "sempryv",
//     requestedPermissions: requestedPermissions,
//     spanButtonID: "pryv-button",
//     callbacks: {
//       signedIn: function(authData) {
//         credentials = authData;
//         // ...
//       }
//     }
//   };
//   pryv.Auth.config.registerURL.host = "reg." + pryvDomain;
//   pryv.Auth.setup(settings);
// }

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
  signOut(callback) {
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    callback();
  }
};
