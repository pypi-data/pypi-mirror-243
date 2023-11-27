from uniplot import plot

from chomp.data_manager import get_weight_diary
from chomp.utils import days_since_today


def stats(days=30, plotwidth=60, interactive=False, num_days_to_average=7):
    """Show moving average plot of weight"""
    data = get_weight_diary()
    datapoints = sorted(data.items())

    if len(datapoints) < num_days_to_average:
        print(f"Only found {len(datapoints)} of weight data.")
        print(f"Creating graph of actual weight points instead of moving average.")
        print()
        num_days_to_average = 1
        title = (f"Weight Over Past {days} Days",)
    else:
        title = (
            f"{num_days_to_average}-day Moving Avg of Weight Over Past {days} Days",
        )

    trailing_xs = []
    trailing_ys = []
    xs = []
    ys = []
    for x, y in datapoints:
        days_ago = days_since_today(x)
        if days_ago > days + (num_days_to_average / 2):
            continue

        trailing_xs.append(int(x))
        trailing_ys.append(float(y["weight"]))
        if len(trailing_xs) < num_days_to_average:
            continue
        if len(trailing_xs) > num_days_to_average:
            trailing_xs.pop(0)
            trailing_ys.pop(0)
        if len(trailing_xs) != num_days_to_average:
            continue

        x_avg = sum(trailing_xs) / num_days_to_average
        x_avg_in_days = days_since_today(x_avg)

        y_avg = sum(trailing_ys) / num_days_to_average

        xs.append(days - x_avg_in_days)
        ys.append(y_avg)

    # yes, y's come first (likely because x's are optional)
    # https://github.com/olavolav/uniplot/blob/814747125ee3be9ab87d2d932f6b310cc46ffad7/uniplot/uniplot.py#L14
    plot(
        ys,
        xs,
        interactive=interactive,
        title=f"{num_days_to_average}-day Moving Avg of Weight Over Past {days} Days",
        width=plotwidth,
    )
