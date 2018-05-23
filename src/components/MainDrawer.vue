<template>
    <v-navigation-drawer v-model="drawer" fixed clipped app>
      <v-list subheader>
        <v-list-tile :to="{name: 'home'}" exact>
          <v-list-tile-action>
            <v-icon>home</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>{{ $t('Home') }}</v-list-tile-content>
        </v-list-tile>
        <v-divider></v-divider>
        <v-subheader>{{ $t('Streams') }}</v-subheader>
        <TreeView v-model="streams"></TreeView>
      </v-list>
    </v-navigation-drawer>
</template>

<script>
import auth from "@/auth";
import TreeView from "@/components/TreeView";

export default {
  components: {
    TreeView
  },
  data() {
    return {
      drawer: false,
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
    this.getStreams();
    if (localStorage.getItem("MainDrawer") !== null) {
      this.drawer = localStorage.getItem("MainDrawer") == "true";
    }
  },
  methods: {
    toggle() {
      this.drawer = !this.drawer;
      localStorage.setItem("MainDrawer", this.drawer);
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
        vm.streams = fstreams;
      });
    }
  }
};
</script>
