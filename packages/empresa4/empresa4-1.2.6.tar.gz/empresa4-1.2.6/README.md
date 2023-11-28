# Installation
`pip install empresa4`

ó, si ya está instalda y hace falta actualizar la versión

`pip install empresa4 -U`


# Publication
`./publish.sh`

# Examples
## Datasets
`from empresa4.datasets import nombres_datasets, get_dataset`

ejecutan nombres_datasets y eso les va a devolver una lista con los datasets disponibles en la librería. 

después hacen por ejemplo

`get_dataset("01_por_cliente")`

y eso les devuelve un DataFrame con todos los sellout ya agrupados por cliente, con periodo y todo lo demás.

## Core
### Calculate Error
Para usar las fórmulas de accuracy que nos pasaron, y que no cometamos errores como nos estuvo pasando:

`from empresa4.core import calculate_error`
`calculate_error(predicciones, valores_reales)`

eso les devuelve un número que es la métrica que vimos en clase. "predicciones" y "valores_reales" tienen que ser dos listas de valores, pueden ser por ejemplo columnas de un dataframe, o arrays de numpy o listas normales

### Produtos Importantes y Clientes Importantes
`from empresa4.core import get_clientes_importantes, get_productos_importantes`

esas dos funciones les devuelven una lista de customer_id y product_id respectivamente que son para los que hay que hacer predicciones por separado. 

Pero aún mejor pueden hacer esto:

`from empresa4.core import filter_productos_importantes, filter_clientes_importantes`

y luego:
`df_importantes = filter_clientes_importantes(df)`
`df_productos_importantes = filter_productos_importantes(df)`

eso devuelve Dataframes de pandas filtrados