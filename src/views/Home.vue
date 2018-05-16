<template>
  <v-content>
<v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card>
        <v-card-title primary-title>
            <h3 class="headline mb-0">Pryv</h3>
        </v-card-title>
        <v-card-actions>
          <span id="pryv-button"></span>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
  </v-content>
</template>

<script>
import pryv from "pryv";

export default {
  mounted: function() {
    var credentials = null;
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
      callbacks: {
        signedIn: function(authData) {
          credentials = authData;
          // ...
        }
      }
    };

    pryv.Auth.config.registerURL.host = "reg." + pryvDomain;
    pryv.Auth.setup(settings);
    credentials;
  }
};
</script>
