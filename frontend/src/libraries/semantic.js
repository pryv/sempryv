import auth from "@/auth";

function update_stream(object, callback) {
  var conn = auth.connection();
  conn.streams.update(object, function(err) {
    callback(err);
  });
}

export function add_code(object, code, callback) {
  if (!object.clientData) {
    object.clientData = {};
  }
  if (!object.clientData["sempryv:codes"]) {
    object.clientData["sempryv:codes"] = [];
  }
  object.clientData["sempryv:codes"].push(code);
  update_stream(object, callback);
}

export function del_code(object, code, callback) {
  var index = object.clientData["sempryv:codes"].indexOf(code);
  object.clientData["sempryv:codes"].splice(index, 1);
  update_stream(object, callback);
}
