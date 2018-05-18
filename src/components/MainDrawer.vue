<template>
    <v-navigation-drawer v-model="drawer" fixed clipped app>
      <v-list subheader>
        <v-list-tile :to="{name: 'home'}" exact>
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>Home</v-list-tile-content>
        </v-list-tile>
        <v-divider></v-divider>
        <pre>{{streams}}</pre>
      </v-list>
    </v-navigation-drawer>
</template>

<script>
import auth from "@/auth";

export default {
  data() {
    return {
      drawer: true,
      streams: ""
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
      console.log(result);
      vm.accessInfo = result;
    });
    this.getStreams();
  },
  methods: {
    toggle() {
      this.drawer = !this.drawer;
    },
    getStreams() {
      var conn = auth.connection();
      var vm = this;

      var options = {
        state: null
      };
      conn.streams.get(options, function(err, streams) {
        var fstreams = streams.map(function(stream) {
          var obj = {
            name: stream.name
          };
          if (stream.children.length) {
            obj.children = stream._children.map(function(children) {
              return {
                name: children.name
              };
            });
          }
          return obj;
        });
        vm.streams = JSON.stringify(fstreams, null, 4);
      });
    }
  }
};
</script>
