<template>
  <v-navigation-drawer v-model="drawer" fixed clipped right app>
    <v-list subheader>
      <v-list-tile color="red" @click="logout()">
        <v-list-tile-action>
          <v-icon>exit_to_app</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>{{ $t("Logout") }}</v-list-tile-content>
      </v-list-tile>
      <v-divider />
    </v-list>
    <v-list subheader>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Domain") }}</v-list-tile-title>
          <v-list-tile-sub-title
            ><v-icon>account_balance</v-icon>
            {{ domain }}</v-list-tile-sub-title
          >
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Username") }}</v-list-tile-title>
          <v-list-tile-sub-title
            ><v-icon>person</v-icon> {{ username }}</v-list-tile-sub-title
          >
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Token") }}</v-list-tile-title>
          <v-list-tile-sub-title
            ><v-icon>vpn_key</v-icon> {{ token }}</v-list-tile-sub-title
          >
        </v-list-tile-content>
      </v-list-tile>
      <v-divider />
    </v-list>
    <v-list>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Type") }}</v-list-tile-title>
          <v-list-tile-sub-title>{{ accessInfo.type }}</v-list-tile-sub-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Application ID") }}</v-list-tile-title>
          <v-list-tile-sub-title>{{ accessInfo.name }}</v-list-tile-sub-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Permissions") }}</v-list-tile-title>
          <v-list-tile-sub-title>&nbsp;</v-list-tile-sub-title>
        </v-list-tile-content>
      </v-list-tile>
      <pre class="info-details">{{
        JSON.stringify(accessInfo.permissions, null, 4)
      }}</pre>
      <v-list-tile>
        <v-list-tile-content>
          <v-list-tile-title>{{ $t("Metadata") }}</v-list-tile-title>
          <v-list-tile-sub-title>&nbsp;</v-list-tile-sub-title>
        </v-list-tile-content>
      </v-list-tile>
      <pre class="info-details">{{
        JSON.stringify(accessInfo.meta, null, 4)
      }}</pre>
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
    domain: function() {
      return localStorage.getItem("domain");
    },
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
    if (localStorage.getItem("InfoDrawer") !== null) {
      this.drawer = localStorage.getItem("InfoDrawer") == "true";
    }
  },
  methods: {
    toggle() {
      this.drawer = !this.drawer;
      localStorage.setItem("InfoDrawer", this.drawer);
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
.info-details {
  font-family: "Exo", sans-serif;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.54);
  padding-right: 16px;
  padding-left: 16px;
  margin-top: -21px;
}
</style>
