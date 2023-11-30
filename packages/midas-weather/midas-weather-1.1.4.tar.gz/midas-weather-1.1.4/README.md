# MIDAS Weather

## Description
This package contains a Midas module providing a simulator for weather data.

Although this package is intendet to be used with Midas, it does not depend on anything Midas-related except for the `midas-util` package.
You can use it in any mosaik simulation scenario.

## Installation
This package will usually be installed automatically together with `midas-mosaik`.
It is available on pypi, you can install it manually with 

```bash
pip install midas-weather
```

## Usage
The complete documentation is available at https://midas-mosaik.gitlab.io/midas.

### Inside of Midas
To use the weather data inside of Midas, add `weather` to your modules

```yaml
my_scenario:
  modules:
    - weather
    - ...
```

and configure it with

```yaml
  weather_params:
    my_weather_scope:
      weather_mapping:
        WeatherCurrent:
          - interpolate: true
            randomize: true
```

If a store module is enabled, the weather module will automatically send all outputs to the store.


### Any mosaik scenario
If you don't use Midas, you can add the `weather` manually to your mosaik scenario file.
First, the entry in the `sim_config`:

```python
sim_config = {
    "WeatherData": {"python": "midas.modules.weather.simulator:WeatherDataSimulator"},
    # ...
}
```

Next, you need to define `start_date` and `step_size`.
The `start_date` is to be provided as ISO datestring and can anything between 2009 and 2022:

```python
start_date = "2021-06-08 14:00:00+0000"
```

The `step_size` can be anything between 1 and 3600. 
Higher values might be possible, but this is untested.

Now, the simulator can be started:

```python
weather_sim = world.start("WeatherData", step_size=900, start_date=start_date)
```

Next, a weather data model can be started:

```python
weather_model = weather_sim.WeatherCurrent(interpolate=True, randomize=True)

```

Finally, the model needs to be connected to other models:

```python
world.connect(weather_model, other_entity, "t_air_deg_celsius", "wind_v_m_per_s")
```

## License
This software is released under the GNU Lesser General Public License (LGPL). See the license file for more information about the details.