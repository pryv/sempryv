<template>
  <v-container
    fluid
    grid-list-lg>
    <v-layout
      row
      wrap>
      <v-flex xs12>
        <v-card v-if="event">
          <v-toolbar
            :style="{ backgroundColor: clientDataColor(event) }"
            dark>
            <v-toolbar-title>{{ event.id }}</v-toolbar-title>
          </v-toolbar>
          <v-container
            fluid
            grid-list-xs>
            <v-layout
              row
              wrap>
              <v-flex
                xs9>
                <h2>{{ $t('Semantic annotations') }}</h2>
                <v-list v-if="codes">
                  <template
                    v-for="(entrycodes, entry) in codes">
                    <v-subheader
                      :key="entry">
                      from {{ streams[entry].name }}:
                    </v-subheader>
                    <template
                      v-for="(code, index) in entrycodes">
                      <v-list-tile
                        :key="entry + index"
                        :to="{name:'stream', params:{id: entry}}">
                        <v-list-tile-content>
                          <v-list-tile-title>{{ code.display }}</v-list-tile-title>
                          <v-list-tile-sub-title>
                            <span class="system">{{ code.system_name }}</span> | {{ code.code }} | <span class="system">{{ code.system_name }}</span>
                          </v-list-tile-sub-title>
                        </v-list-tile-content>
                      </v-list-tile>
                      <v-divider
                        :key="entry + index + 'divider'"/>
                    </template>
                  </v-subheader></template>
                </v-list>
              </v-flex>
              <v-flex
                d-flex
                xs3
                style="border-left: solid 1px gray; overflow-x: auto;">
                <v-list dense>
                  <v-subheader>
                    {{ $t('Navigation') }}
                  </v-subheader>
                  <v-list-tile
                    :to="{name:'stream', params:{id: event.streamId}}">
                    <v-list-tile-action>
                      <v-icon>arrow_upward</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                      {{ event.streamId }}
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-subheader>{{ $t('Event info') }}</v-subheader>
                  <v-list-tile>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ $t('Id') }}
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{ event.id }}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ $t('Type') }}
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{ event.type }}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ $t('Content') }}
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{ event.content }}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ $t('Time') }}
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{ formatTime(event.time) }}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ $t('Client data') }}
                      </v-list-tile-title>
                    </v-list-tile-content>
                  </v-list-tile>
                  <pre class="event-details">{{ JSON.stringify(event.clientData, null, 4) }}</pre>
                </v-list>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import auth from "@/auth";
import Semantic from "@/components/Semantic";
import moment from "moment";
import { get_event_codes } from "@/libraries/semantic";
import Vue from "vue";

export default {
  components: {
    Semantic
  },
  data() {
    return {
      event: null,
      codes: {},
      streams: {}
    };
  },
  mounted() {
    this.refreshEvent();
  },
  beforeRouteUpdate(to, from, next) {
    this.getEvent(to.params.id);
    next();
  },
  methods: {
    getEvent(eventId) {
      var conn = auth.connection();
      var vm = this;
      conn.events.getOne(eventId, function(err, event) {
        vm.event = event;
        vm.codes = {};
        vm.streams = {};
        get_event_codes(event, function(err, codes, stream) {
          Vue.set(vm.codes, stream.id, codes);
          Vue.set(vm.streams, stream.id, stream);
        });
      });
    },
    refreshEvent() {
      this.getEvent(this.$route.params.id);
    },
    clientDataColor(event) {
      if (event.clientData) {
        if (event.clientData["pryv-browser:bgColor"]) {
          return event.clientData["pryv-browser:bgColor"];
        }
      }
      return "gray";
    },
    formatTime(time) {
      return moment.unix(time).format("YYYY-MM-DD HH:MM:SS");
    }
  }
};
</script>

<style>
.event-details {
  font-family: "Exo", sans-serif;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.54);
  padding-right: 16px;
  padding-left: 16px;
  max-height: 300px;
  overflow-y: auto;
}
</style>
