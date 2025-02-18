import auth from "@/auth";

const namespace = "sempryv";

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
  var key_codes = namespace + ":codes";
  var key_rec = namespace + ":recursive";
  getStream(streamId, function(err, stream) {
    if (
      stream &&
      stream.clientData &&
      stream.clientData[key_codes] &&
      (stream.clientData[key_rec] || event.streamId == streamId)
    ) {
      callback(null, stream.clientData[key_codes][event.type], stream);
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
  var key = namespace + ":codes";
  if (!stream.clientData) {
    stream.clientData = {};
  }
  if (!stream.clientData[key]) {
    stream.clientData[key] = {};
  }
  if (!stream.clientData[key][type]) {
    stream.clientData[key][type] = [];
  }
  stream.clientData[key][type].push(code);
  update_stream(stream, callback);
}

export function del_code(stream, type, code, callback) {
  var key = namespace + ":codes";
  var index = stream.clientData[key][type].indexOf(code);
  stream.clientData[key][type].splice(index, 1);
  if (stream.clientData[key][type].length == 0) {
    delete stream.clientData[key][type];
  }
  if (Object.keys(stream.clientData[key]).length == 0) {
    stream.clientData[key] = null;
  }
  update_stream(stream, callback);
}

export function get_event_types(streamId, callback) {
  var conn = auth.connection();
  var filter = {
    streams: [streamId],
    limit: 0
  };
  conn.events.get(filter, function(err, events) {
    callback(Array.from(new Set(events.map(event => event.type))));
  });
}

export function get_recursive(stream) {
  var key = namespace + ":recursive";
  if (stream && stream.clientData && stream.clientData[key]) {
    return stream.clientData[key];
  }
  return false;
}

export function set_recursive(stream, value, callback) {
  var key = namespace + ":recursive";
  stream.clientData[key] = value;
  update_stream(stream, callback);
}

function _full_path_rec(streams, streamId, suffix) {
  var stream = streams.filter(stream => {
    return stream.id == streamId;
  })[0];
  var name = stream.name;
  if (stream.parentId) {
    return _full_path_rec(streams, stream.parentId, "/" + name + suffix);
  } else {
    return "/" + name + suffix;
  }
}

export function full_path(streamId, callback) {
  var conn = auth.connection();
  var options = {};
  conn.streams.getFlatenedObjects(options, function(err, streams) {
    var path = _full_path_rec(streams, streamId, "");
    callback(err, path);
  });
}

export default {
  add_code,
  del_code,
  get_event_codes,
  get_event_types,
  get_recursive,
  set_recursive,
  full_path
};
