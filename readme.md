<!-- @format -->

# Compartmental models in epidemiology

## Use model

```python
model = SEISModel(population=population,
                  per_capita_natural_death_rate=death_rate, per_capita_birth_rate=birth_rate)
```

## Draw graph and save

```python
model.draw_graph_at(days=50)
```

## Animated graph

```python
model.animate_graph()
```

## Add new model

Subclass BaseModel like this

```python
class SEIRModel(BaseModel):
    pass
```

## Example output

See website

- Data: https://population.un.org/wpp/Download/Standard/CSV/