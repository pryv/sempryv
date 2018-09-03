import auth from "@/auth";

function update_stream(object, callback) {
  var conn = auth.connection();
  conn.streams.update(object, function(err) {
    callback(err);
  });
}

export function add_code(object, type, code, callback) {
  if (!object.clientData) {
    object.clientData = {};
  }
  if (!object.clientData["sempryv:codes"]) {
    object.clientData["sempryv:codes"] = {};
  }
  if (!object.clientData["sempryv:codes"][type]) {
    object.clientData["sempryv:codes"][type] = [];
  }
  object.clientData["sempryv:codes"][type].push(code);
  update_stream(object, callback);
}

export function del_code(object, type, code, callback) {
  var index = object.clientData["sempryv:codes"][type].indexOf(code);
  object.clientData["sempryv:codes"][type].splice(index, 1);
  if (object.clientData["sempryv:codes"][type].length == 0) {
    delete object.clientData["sempryv:codes"][type];
  }
  update_stream(object, callback);
}
