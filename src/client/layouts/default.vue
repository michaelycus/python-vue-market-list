<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer"
                         app>
      <v-list dense>
        <v-list-item link
                     nuxt
                     to="/">
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link
                     nuxt
                     to="/categories">
          <v-list-item-action>
            <v-icon>mdi-tag-minus-outline</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Categorias</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link
                     nuxt
                     to="/products">
          <v-list-item-action>
            <v-icon>mdi-cart-arrow-down</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Produtos</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app
               color="indigo"
               dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Mercado</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <nuxt />
    </v-main>
    <v-footer color="indigo"
              app>
      <span class="white--text">&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  props: {
    source: String,
  },
  data: () => ({
    drawer: null,
  }),
}
</script>
