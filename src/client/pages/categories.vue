<template>
  <v-card class="mx-5 mt-5">
    <v-data-table :headers="headers"
                  :items="categories"
                  sort-by="name"
                  class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat
                   color="white">
          <v-toolbar-title>Categorias</v-toolbar-title>
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
                     v-on="on">Nova Categoria</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field v-model="editedItem.name"
                                    label="Nome da Categoria"></v-text-field>
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
        <v-card-title class="headline">Excluir categoria
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
      { text: 'Ações', value: 'actions', sortable: false },
    ],
    editedIndex: -1,
    editedItem: {
      name: '',
    },
    defaultItem: {
      name: '',
    },
    categories: []
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nova Categoria' : 'Editar'
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },
  },

  async asyncData ({ $axios }) {
    let categories = await $axios.$get('api/categories/')

    return { categories }
  },

  methods: {
    editItem (item) {
      this.editedIndex = this.categories.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem (item) {
      this.editedIndex = this.categories.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.confirmDeleteDialog = true
    },

    confirmDelete (item) {
      this.confirmDeleteDialog = false
      this.categories.splice(this.editedIndex, 1)

      this.$axios.$delete(`api/categories/${this.editedItem.id}`)
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
        Object.assign(this.categories[this.editedIndex], this.editedItem)

        this.$axios.$put(`api/categories/${this.editedItem.id}/`, {
          'id': this.editedItem.id,
          'name': this.editedItem.name
        }).catch(errors => {
          console.log(errors)
        })
      } else {
        this.$axios.$post(`api/categories/`, {
          'id': this.editedItem.id,
          'name': this.editedItem.name
        }).then(response => {
          this.categories.push(response)
        }).catch(errors => {
          console.log(errors)
        })
      }
      this.close()
    },
  },
}
</script>

