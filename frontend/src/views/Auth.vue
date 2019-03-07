<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex sm12 md8>
        <v-card>
          <v-toolbar color="primary" dark>
            <v-toolbar-title>{{
              $t("Authentication required")
            }}</v-toolbar-title>
            <v-spacer />
            <v-btn v-if="!pryvSignedin" color="pryv" dark @click="pryvSignIn()">
              <img src="../assets/logo-pryv.png" />
              &nbsp;
              {{ $t("Sign In @{domain}", { domain: domain }) }}
              <v-icon right dark>
                person
              </v-icon>
            </v-btn>
            <v-btn v-if="pryvSignedin" color="pryv" dark @click="pryvSignOut()">
              <img src="../assets/logo-pryv.png" />
              &nbsp;
              {{
                $t("Sign out {username}@{domain}", {
                  username: pryvUsername,
                  domain: domain
                })
              }}
              <v-icon right dark>
                exit_to_app
              </v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text>
            <v-alert v-model="alert" :type="alertType">
              {{ alertMessage }}
            </v-alert>
            <v-form>
              <v-combobox
                v-model="domain"
                :items="domains"
                :label="$t('Domain')"
                single-line
                prepend-icon="account_balance"
                @input="domainChanged()"
              />
              <v-text-field
                v-model="username"
                :label="$t('Username')"
                prepend-icon="person"
                type="text"
                @keyup.enter.native="connect()"
                @input="resetAlert()"
              />
              <v-text-field
                v-model="token"
                :label="$t('Token')"
                prepend-icon="vpn_key"
                type="text"
                @keyup.enter.native="connect()"
                @input="resetAlert()"
              />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              v-if="pryvSignedin"
              color="pryv"
              dark
              @click="connectWithPryv()"
            >
              <img src="../assets/logo-pryv.png" />
              &nbsp;
              {{ $t("Connect with Pryv") }}
            </v-btn>
            <v-btn color="primary" @click="connect()">
              <v-icon left dark>
                arrow_forward
              </v-icon>
              {{ $t("Connect") }}
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
      domain: "",
      domains: ["pryv.me", "pryv.li"],
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
    this.domain = localStorage.domain || "pryv.me";
    this.username = localStorage.username;
    this.token = localStorage.token;
    this.setup(this.domain);
  },
  methods: {
    connect() {
      auth.login(this.domain, this.username, this.token);
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
    domainChanged() {
      this.setup(this.domain);
      this.resetAlert();
    },
    setup(domain) {
      auth.pryvSetup(
        domain,
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

<style scoped></style>
