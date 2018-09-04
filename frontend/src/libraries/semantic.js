import auth from "@/auth";

const namespace = "sempryv:codes";

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
  if (!object.clientData[namespace]) {
    object.clientData[namespace] = {};
  }
  if (!object.clientData[namespace][type]) {
    object.clientData[namespace][type] = [];
  }
  object.clientData[namespace][type].push(code);
  update_stream(object, callback);
}

export function del_code(object, type, code, callback) {
  var index = object.clientData[namespace][type].indexOf(code);
  object.clientData[namespace][type].splice(index, 1);
  if (object.clientData[namespace][type].length == 0) {
    delete object.clientData[namespace][type];
  }
  if (Object.keys(object.clientData[namespace]).length == 0) {
    object.clientData[namespace] = null;
  }
  update_stream(object, callback);
}
