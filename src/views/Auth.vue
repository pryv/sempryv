<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex sm12 md8>
        <v-card>
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Authentication required</v-toolbar-title>
            <v-spacer></v-spacer>
                <v-btn color="pryv" dark
                  v-if="!pryvSignedin"
                  @click="pryvSignIn()">
                  <img src="../assets/logo-pryv.png"/>&nbsp;
                  Pryv sign in
                  <v-icon right dark>person</v-icon>
                </v-btn>
                <v-btn flat color="tran" dark
                  v-if="pryvSignedin"
                  @click="loadPryvCredentials()">
                  <v-icon left dark>arrow_downward</v-icon>
                  Use Pryv credentials
                </v-btn>
                <v-btn color="pryv" dark
                  v-if="pryvSignedin"
                  @click="pryvSignOut()">
                  <img src="../assets/logo-pryv.png"/>&nbsp;
                  Sign out {{pryvUsername}}
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
                name="username"
                label="Username"
                type="text"
                v-model="username"
                @keyup.enter.native="connect()"
                @input="resetAlert()"></v-text-field>
              <v-text-field
                prepend-icon="vpn_key"
                name="token"
                label="Token"
                type="text"
                v-model="token"
                @keyup.enter.native="connect()"
                @input="resetAlert()"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="connect()">
              <v-icon left dark>arrow_forward</v-icon>
              Connect
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
          this.alertMessage = "Authentication successful";
          this.alert = true;
          setTimeout(() => {
            this.$router.push({ name: "home" });
          }, 1000);
        },
        () => {
          this.alertType = "error";
          this.alertMessage = "Authentication failed";
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
    loadPryvCredentials() {
      var credentials = auth.pryvCredentials();
      this.username = credentials.username;
      this.token = credentials.token;
    },
    resetAlert() {
      this.alert = false;
    }
  }
};
</script>

<style scoped>
</style>
