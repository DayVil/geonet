from examples.boundary_estimation.dynamic_rain import dynamic_rain_run
from examples.boundary_estimation.propagating_rain import propagating_rain_run
from examples.boundary_estimation.static_rain import static_rain_run


def main():
    static_rain_run()
    dynamic_rain_run()
    propagating_rain_run()


if __name__ == "__main__":
    main()
