<template>
  <v-card class="mx-5 mt-5">
    <v-data-table :headers="headers"
                  :items="products"
                  sort-by="name"
                  class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat
                   color="white">
          <v-toolbar-title>Produtos</v-toolbar-title>
          <v-divider class="mx-4"
                     inset
                     vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog"
                    max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary"
                     dark
                     class="mb-2"
                     v-bind="attrs"
                     v-on="on">Novo Produto</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="6">
                      <v-text-field v-model="editedItem.name"
                                    label="Nome do Produto"></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="editedItem.brand"
                                    label="Marca"></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-select :items="categories"
                                item-text="name"
                                item-value="id"
                                v-model="editedItem.category"
                                label=" - Categoria - "></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1"
                       text
                       @click="close">Cancelar</v-btn>
                <v-btn color="blue darken-1"
                       text
                       @click="save">Salvar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template #item.category="{ item }">
        <v-chip :color="categoryColor(item.category)"
                dark>
          {{ categoryName(item.category) }}</v-chip>
      </template>
      <template #item.actions="{ item }">
        <v-icon small
                class="mr-2"
                @click="editItem(item)">
          mdi-pencil
        </v-icon>
        <v-icon small
                @click="deleteItem(item)">
          mdi-delete
        </v-icon>
      </template>
      <template #no-data>
        <v-btn color="primary"
               @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="confirmDeleteDialog"
              max-width="290">
      <v-card>
        <v-card-title class="headline">Excluir produto
          <v-icon>mdi-delete</v-icon>
        </v-card-title>

        <v-card-text>
          Tem certeza que deseja deletar esse item?
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="gray darken-1"
                 text
                 @click="confirmDeleteDialog = false">
            Cancelar
          </v-btn>

          <v-btn color="red darken-1"
                 text
                 @click="confirmDelete">
            Deletar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>

</template>

<script>
export default {
  data: () => ({
    dialog: false,
    confirmDeleteDialog: false,
    headers: [
      {
        text: 'Nome',
        align: 'start',
        sortable: false,
        value: 'name',
      },
      { text: 'Marca', value: 'brand', sortable: true },
      { text: 'Categoria', value: 'category', sortable: true },
      { text: 'Ações', value: 'actions', sortable: false },
    ],
    editedIndex: -1,
    editedItem: {
      name: '',
      brand: '',
      category: 0,
    },
    defaultItem: {
      name: '',
      brand: '',
      category: 0,
    },
    products: [],
    categories: []
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Novo Produto' : 'Editar'
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },
  },

  async asyncData ({ $axios }) {
    let categories = await $axios.$get('api/categories/')
    let products = await $axios.$get('api/products/')

    return { categories, products }
  },

  methods: {
    categoryName (id) {
      return this.categories.find(c => c.id == id).name
    },

    categoryColor (id) {
      let colors = ['orange', 'green', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue',
        'cyan', 'teal', 'light-green', 'lime', 'yellow', 'amber', 'deep-orange']
      return colors[id % colors.length]
    },

    editItem (item) {
      this.editedIndex = this.products.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem (item) {
      this.editedIndex = this.products.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.confirmDeleteDialog = true
    },

    confirmDelete (item) {
      this.confirmDeleteDialog = false
      this.products.splice(this.editedIndex, 1)

      this.$axios.$delete(`api/products/${this.editedItem.id}`)
        .catch(errors => {
          console.log(errors)
        })

      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.products[this.editedIndex], this.editedItem)

        this.$axios.$put(`api/products/${this.editedItem.id}/`, {
          'id': this.editedItem.id,
          'name': this.editedItem.name,
          'category': this.editedItem.category,
          'brand': this.editedItem.brand,
        }).catch(errors => {
          console.log(errors)
        })
      } else {
        this.$axios.$post(`api/products/`, {
          'name': this.editedItem.name,
          'category': this.editedItem.category,
          'brand': this.editedItem.brand,
        }).then(response => {
          this.products.push(response)
        }).catch(errors => {
          console.log(errors)
        })
      }
      this.close()
    },
  },
}
</script>

