<template>
  <v-container class="grey lighten-5">
    <v-row>
      <v-col cols=10>
        <v-row no-gutters
               v-for="category in categories"
               :key="category.id">
          <v-col cols="2"
                 class="text-center">
            <h2>{{ category.name }}</h2>
          </v-col>
          <v-col cols="10"
                 class="d-flex flex-row flex-wrap">
            <div v-for="product in products"
                 :key="product.id">

              <div v-if="product.category == category.id"
                   class="pa-1 flex-column"
                   style="width: 180px; height: 90px">

                <product-item @increment="incrementProduct"
                              @decrement="decrementProduct"
                              :product="product"></product-item>

              </div>
            </div>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols=2
             class="text-center">
        <v-row align="center">
          <v-col class="text-center"
                 cols="12">
            <v-btn color="success"
                   @click="generateList">Gerar & salvar
              <v-icon>
                mdi-arrow-down-thick
              </v-icon>
            </v-btn>
          </v-col>
          <v-col class="text-center"
                 cols="12">
            <v-textarea outlined
                        name="input-7-4"
                        label="Lista Completa"
                        rows="20"
                        :value="completeList">
            </v-textarea>
          </v-col>
          <v-col cols="12">
            <v-btn color="warning"
                   @click="clearList">
              <v-icon>mdi-broom</v-icon>Limpar lista
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import ProductItem from '../components/ProductItem'

export default {
  components: {
    ProductItem
  },

  data () {
    return {
      categories: [],
      products: [],
      completeList: ' - Lista vazia -',
    }
  },

  async fetch () {
    this.categories = await fetch(
      'http://127.0.0.1:8000/api/categories/'
    ).then(res => res.json())
    this.products = await fetch(
      'http://127.0.0.1:8000/api/products/'
    ).then(res => res.json())

    this.products.map(p => p.quantity = 0)
    this.loadFromLocalStorage()
  },

  methods: {
    incrementProduct (productId) {
      this.products.find(p => p.id == productId).quantity++
    },

    decrementProduct (productId) {
      this.products.find(p => p.id == productId).quantity--
    },

    generateList () {
      this.completeList = ''
      this.categories.forEach(category => {
        let elements = []
        this.products.forEach(p => {
          if (p.category == category.id && p.quantity > 0) {
            elements.push(p)
          }
        });
        if (elements.length > 0) {
          this.completeList += '-= ' + category.name + ' =-\n'

          elements.forEach(p => {
            if (p.quantity > 0) {
              this.completeList += '- ' + p.quantity + ' ' + p.name + (p.brand ? ' (' + p.brand + ') ' : '') + '\n'
            }
          });
          this.completeList += '\n'
        }
      });

      this.saveOnLocalStorage()
    },

    clearList () {
      window.localStorage.clear();
      this.$router.go()
    },

    saveOnLocalStorage () {
      localStorage.setItem('products', JSON.stringify(this.products))
    },

    loadFromLocalStorage () {
      var listProducts = localStorage.getItem('products');

      if (listProducts != null) {
        JSON.parse(listProducts).forEach(product => {
          if (product.quantity > 0) {
            this.products.find(p => p.id == product.id).quantity = product.quantity
          }
        });
      }
    }
  },
}
</script>
