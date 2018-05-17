<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex sm12 md8>
        <v-card>
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Authentication required</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
              <v-alert v-model="alert" :type="alertType" dismissible>
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
              <div class="text-xs-center">
              <v-btn color="pryv" dark>
                <img src="../assets/logo-pryv.png"/>&nbsp;
                Pryv sign-In
              </v-btn>
              <v-btn color="primary" @click="connect()">
                <v-icon left dark>arrow_forward</v-icon>
                Connect
              </v-btn>
              </div>
            </v-form>
          </v-card-text>
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
      alertMessage: "Authentication Failed"
    };
  },
  methods: {
    connect() {
      localStorage.setItem("username", this.username);
      localStorage.setItem("token", this.token);

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
    resetAlert() {
      this.alert = false;
    }
  }
};
</script>

<style scoped>
</style>
