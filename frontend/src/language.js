import Vue from "vue";
import VueI18n from "vue-i18n";
import moment from "moment";

import en from "./assets/i18n/en.json";
import fr from "./assets/i18n/fr.json";

Vue.use(VueI18n);

var messages = {
  en: en,
  fr: fr
};

// Fix issue with moment case
moment.defineLocale("fr-ucase", {
  parentLocale: "fr",
  weekdays: "Dimanche_Lundi_Mardi_Mercredi_Jeudi_Vendredi_Samedi".split("_")
});

export var momentLocales = {
  en: "en",
  fr: "fr-ucase"
};

export var i18n = new VueI18n({
  locale: "en",
  fallbackLocale: "en",
  messages
});
