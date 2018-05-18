<template>
    <v-navigation-drawer v-model="drawer" fixed clipped right app>
      <v-list subheader>
        <v-list-tile @click="logout()" color="red">
          <v-list-tile-action>
            <v-icon>exit_to_app</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>Logout</v-list-tile-content>
        </v-list-tile>
        <v-divider></v-divider>
      </v-list>
      <v-list subheader>
        <v-list-tile>
          <v-list-tile-content>
              <v-list-tile-title>Username</v-list-tile-title>
              <v-list-tile-sub-title><v-icon>person</v-icon> {{username}}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
              <v-list-tile-title>Token</v-list-tile-title>
              <v-list-tile-sub-title><v-icon>vpn_key</v-icon> {{token}}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-divider></v-divider>
      </v-list>
      <v-list>
        <v-list-tile>
          <v-list-tile-content>
              <v-list-tile-title>Type</v-list-tile-title>
              <v-list-tile-sub-title>{{accessInfo.type}}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
              <v-list-tile-title>Application ID</v-list-tile-title>
              <v-list-tile-sub-title>{{accessInfo.name}}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile>
          <v-list-tile-content>
              <v-list-tile-title>Permissions</v-list-tile-title>
              <v-list-tile-sub-title>&nbsp;</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <pre class="list-details">{{JSON.stringify(accessInfo.permissions, null, 4)}}</pre>
        <v-list-tile>
          <v-list-tile-content>
              <v-list-tile-title>Meta</v-list-tile-title>
              <v-list-tile-sub-title>&nbsp;</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <pre class="list-details">{{JSON.stringify(accessInfo.meta, null, 4)}}</pre>
      </v-list>
    </v-navigation-drawer>
</template>

<script>
import auth from "@/auth";

export default {
  data() {
    return {
      drawer: false,
      accessInfo: {}
    };
  },
  computed: {
    username: function() {
      return localStorage.getItem("username");
    },
    token: function() {
      return localStorage.getItem("token");
    }
  },
  mounted() {
    var vm = this;
    auth.connection().accessInfo(function(err, result) {
      vm.accessInfo = result;
    });
  },
  methods: {
    toggle() {
      this.drawer = !this.drawer;
    },
    logout() {
      auth.logout();
      this.authenticated = false;
      this.$router.push({ name: "auth" });
    }
  }
};
</script>

<style>
.list-details {
  font-family: "Exo", sans-serif;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.54);
  padding-right: 16px;
  padding-left: 16px;
  margin-top: -21px;
}
</style>
