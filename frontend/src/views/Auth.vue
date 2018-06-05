<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex sm12 md8>
        <v-card>
          <v-toolbar color="primary" dark>
            <v-toolbar-title>{{ $t('Authentication required') }}</v-toolbar-title>
            <v-spacer></v-spacer>
                <v-btn color="pryv" dark
                  v-if="!pryvSignedin"
                  @click="pryvSignIn()">
                  <img src="../assets/logo-pryv.png"/>&nbsp;
                  {{ $t('Pryv Sign In') }}
                  <v-icon right dark>person</v-icon>
                </v-btn>
                <v-btn color="pryv" dark
                  v-if="pryvSignedin"
                  @click="pryvSignOut()">
                  <img src="../assets/logo-pryv.png"/>&nbsp;
                  {{ $t('Sign out {username}', {username: pryvUsername}) }}
                  <v-icon right dark>exit_to_app</v-icon>
                </v-btn>
          </v-toolbar>
          <v-card-text>
              <v-alert v-model="alert" :type="alertType">
                {{alertMessage}}
              </v-alert>
            <v-form>
              <v-text-field
                prepend-icon="person"
                :label="$t('Username')"
                type="text"
                v-model="username"
                @keyup.enter.native="connect()"
                @input="resetAlert()"></v-text-field>
              <v-text-field
                prepend-icon="vpn_key"
                :label="$t('Token')"
                type="text"
                v-model="token"
                @keyup.enter.native="connect()"
                @input="resetAlert()"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="pryv" dark
              v-if="pryvSignedin"
              @click="connectWithPryv()">
              <img src="../assets/logo-pryv.png"/>&nbsp;
              {{ $t('Connect with Pryv') }}
            </v-btn>
            <v-btn color="primary" @click="connect()">
              <v-icon left dark>arrow_forward</v-icon>
              {{ $t('Connect with token') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import auth from "@/auth";

export default {
  data() {
    return {
      username: "",
      token: "",
      alert: false,
      alertType: "error",
      alertMessage: "Authentication Failed",
      pryvSignedin: false,
      pryvUsername: ""
    };
  },
  mounted() {
    auth.pryvSetup(
      authData => {
        this.pryvSignedin = true;
        this.pryvUsername = authData.username;
      },
      () => {
        this.pryvSignedin = false;
        this.username = "";
        this.token = "";
      }
    );
  },
  methods: {
    connect() {
      auth.login(this.username, this.token);
      auth.isConnected(
        () => {
          this.alertType = "success";
          this.alertMessage = this.$t("Authentication successful");
          this.alert = true;
          setTimeout(() => {
            this.$router.push({ name: "home" });
          }, 1000);
        },
        () => {
          this.alertType = "error";
          this.alertMessage = this.$t("Authentication failed");
          this.alert = true;
        }
      );
    },
    pryvSignIn() {
      auth.signIn();
    },
    pryvSignOut() {
      auth.signOut();
    },
    connectWithPryv() {
      var credentials = auth.pryvCredentials();
      this.username = credentials.username;
      this.token = credentials.token;
      this.connect();
    },
    resetAlert() {
      this.alert = false;
    }
  }
};
</script>

<style scoped>
</style>
