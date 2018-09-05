import auth from "@/auth";

const namespace = "sempryv:codes";

function getStream(streamId, callback) {
  var conn = auth.connection();
  var options = { streamId: streamId };
  conn.streams.getFlatenedObjects(options, function(err, streams) {
    var stream = streams.filter(stream => {
      return stream.id == streamId;
    })[0];
    callback(err, stream);
  });
}

function update_stream(stream, callback) {
  var conn = auth.connection();
  conn.streams.update(stream, function(err) {
    callback(err);
  });
}

function get_event_codes_rec(streamId, event, callback) {
  getStream(streamId, function(err, stream) {
    if (stream && stream.clientData && stream.clientData["sempryv:codes"]) {
      callback(null, stream.clientData["sempryv:codes"][event.type], stream);
    }
    if (stream && stream.parentId) {
      get_event_codes_rec(stream.parentId, event, callback);
    }
  });
}

export function get_event_codes(event, callback) {
  get_event_codes_rec(event.streamId, event, callback);
}

export function add_code(stream, type, code, callback) {
  if (!stream.clientData) {
    stream.clientData = {};
  }
  if (!stream.clientData[namespace]) {
    stream.clientData[namespace] = {};
  }
  if (!stream.clientData[namespace][type]) {
    stream.clientData[namespace][type] = [];
  }
  stream.clientData[namespace][type].push(code);
  update_stream(stream, callback);
}

export function del_code(stream, type, code, callback) {
  var index = stream.clientData[namespace][type].indexOf(code);
  stream.clientData[namespace][type].splice(index, 1);
  if (stream.clientData[namespace][type].length == 0) {
    delete stream.clientData[namespace][type];
  }
  if (Object.keys(stream.clientData[namespace]).length == 0) {
    stream.clientData[namespace] = null;
  }
  update_stream(stream, callback);
}
