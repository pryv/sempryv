<template>
  <v-container
    fluid
    grid-list-lg>
    <v-layout
      row
      wrap>
      <v-flex xs12>
        <v-card v-if="stream">
          <v-toolbar
            :style="{ backgroundColor: clientDataColor(stream) }"
            dark>
            <v-toolbar-title>{{ stream.name }}</v-toolbar-title>
          </v-toolbar>
          <v-container
            fluid
            grid-list-xs>
            <v-layout
              row
              wrap>
              <v-flex
                xs9>
                <semantic
                  v-model="stream.id"
                  @updated="refreshStream()"
                />
              </v-flex>
              <v-flex
                d-flex
                xs3
                style="border-left: solid 1px gray; overflow-x: auto;">
                <v-list dense>
                  <v-subheader
                    v-if="parent || children.length > 0">
                    {{ $t('Navigation') }}
                  </v-subheader>
                  <v-list-tile
                    v-if="parent"
                    :to="{name:'stream', params:{id: parent.id}}">
                    <v-list-tile-action>
                      <v-icon>arrow_upward</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                      {{ parent.id }}
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-divider v-if="parent && children.length > 0"/>
                  <v-list-tile
                    v-for="child in children"
                    :key="child.id"
                    :to="{name:'stream', params:{id: child.id}}">
                    <v-list-tile-action>
                      <v-icon>subdirectory_arrow_right</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>{{ child.name }}</v-list-tile-content>
                  </v-list-tile>
                  <v-subheader>{{ $t('Stream info') }}</v-subheader>
                  <v-list-tile>
                    <v-list-tile-title>
                      {{ $t('Id') }}
                    </v-list-tile-title>
                    <v-list-tile-sub-title>
                      {{ stream.id }}
                    </v-list-tile-sub-title>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-title>
                      {{ $t('Name') }}
                    </v-list-tile-title>
                    <v-list-tile-sub-title>
                      {{ stream.name }}
                    </v-list-tile-sub-title>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-title>
                      {{ $t('Client data') }}
                    </v-list-tile-title>
                  </v-list-tile>
                  <pre class="stream-details">{{ JSON.stringify(stream.clientData, null, 4) }}</pre>
                </v-list>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
      <v-flex
        v-if="events.length > 0"
        xs12>
        <v-card>
          <v-toolbar
            :style="{ color: clientDataColor(stream) }"
            card
            height="40"
            dense>
            <v-toolbar-title> {{ $t('Events') }}</v-toolbar-title>
          </v-toolbar>
          <v-list two-line>
            <div
              v-for="(event, index) in events"
              :key="index">
              {{ event.content }} || {{ event.id }} || {{ event.trashed }}
            </div>
          </v-list>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import auth from "@/auth";
import Semantic from "@/components/Semantic";

export default {
  components: {
    Semantic
  },
  data() {
    return {
      stream: null,
      events: [],
      streams: []
    };
  },
  computed: {
    children() {
      if (!this.stream) {
        return [];
      }
      return this.stream.childrenIds.map(
        childrenId => this.streams.filter(stream => stream.id == childrenId)[0]
      );
    },
    parent() {
      if (!this.stream || !this.stream.parentId) {
        return null;
      }
      return this.streams.filter(
        stream => stream.id == this.stream.parentId
      )[0];
    }
  },
  mounted() {
    this.refreshStream();
  },
  beforeRouteUpdate(to, from, next) {
    this.getStream(to.params.id);
    next();
  },
  methods: {
    getStream(streamId) {
      var conn = auth.connection();
      var options = { id: streamId };
      var vm = this;
      conn.streams.getFlatenedObjects(options, function(err, streams) {
        vm.streams = streams;
        vm.stream = streams.filter(stream => {
          return stream.id == streamId;
        })[0];
        var filter = {
          streams: [vm.stream.id]
        };
        conn.events.get(filter, function(err, events) {
          vm.events = events;
        });
      });
    },
    refreshStream() {
      this.getStream(this.$route.params.id);
    },
    clientDataColor(stream) {
      if (stream.clientData) {
        if (stream.clientData["pryv-browser:bgColor"]) {
          return stream.clientData["pryv-browser:bgColor"];
        }
      }
      return "gray";
    }
  }
};
</script>

<style>
.stream-details {
  font-family: "Exo", sans-serif;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.54);
  padding-right: 16px;
  padding-left: 16px;
}
</style>
