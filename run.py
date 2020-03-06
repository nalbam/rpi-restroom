import argparse
import boto3
import os
import time

import RPi.GPIO as gpio


GPIO_OUT = 17
GPIO_IN = 27

INTERVAL = 0.5

AWS_REGION = os.environ.get("AWSREGION", "ap-northeast-2")
TABLE_NAME = os.environ.get("TABLE_NAME", "restroom-demo")


ddb = boto3.resource("dynamodb", region_name=AWS_REGION)
tbl = ddb.Table(TABLE_NAME)


def parse_args():
    p = argparse.ArgumentParser(description="restroom")
    p.add_argument("--gpio-out", type=int, default=GPIO_OUT, help="gpio-out")
    p.add_argument("--gpio-in", type=int, default=GPIO_IN, help="gpio-in")
    p.add_argument("--interval", type=float, default=INTERVAL, help="interval")


def main():
    args = parse_args()

    gpio.setmode(gpio.BCM)

    print(args)
    print(args.gpio_out, args.gpio_in, args.interval)

    gpio.setup(args.gpio_out, gpio.OUT)
    gpio.setup(args.gpio_in, gpio.IN)

    try:
        while True:
            gpio.output(args.gpio_out, False)
            time.sleep(args.interval)

            gpio.output(args.gpio_out, True)
            time.sleep(0.00001)
            gpio.output(args.gpio_out, False)

            while gpio.input(args.gpio_in) == 0:
                continue
            pulse_start = time.time()

            while gpio.input(args.gpio_in) == 1:
                continue
            pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)

            print("Distance", distance, "cm")
    except:
        gpio.cleanup()


if __name__ == "__main__":
    main()
