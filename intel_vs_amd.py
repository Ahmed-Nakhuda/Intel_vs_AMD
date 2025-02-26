import matplotlib.pyplot as plt

# max cost
MAX_D=3000;

# store cpu data
intel=[]; amd=[];
best_intel=None; best_amd=None;
max_intel_bench=0; max_amd_bench=0;

with open('a3_multi_core_cpu_data.txt') as r:
 for line in r:
        # split the words and apply an index to each word
        parts = line.split()
        for i, part in enumerate(parts):

            # find percentage
            if part.startswith("(") and part.endswith("%)"):
                cpu_percent = part

                # extract all words before percentage and join to make name
                cpu_name = " ".join(parts[:i])

                # benchmark comes after percent
                cpu_mark = parts[i + 1].replace(',', '')

                # price comes after benchmark
                price = parts[i + 2].strip('$*').replace(',', '')
                if price != "NA":
                    if cpu_name.startswith("Intel"):
                        intel.append([cpu_name, cpu_percent, cpu_mark, price])
                    else:
                        amd.append([cpu_name, cpu_percent, cpu_mark, price])


def best(cpu_list):
    """Function to find the cpu with the highest benchmark under the
       specified price

    Keyword arguments:
    cpu_list -- takes a list of either the Intel or AMD cpu

    Returns:
    The best cpu and its benchmark score
    """

    # store the best cpu and max benchmark found
    best_cpu = None; max_cpu_benchmark = 0

    # find the cpu under MAX_D that has the highest benchmark
    for cpu in cpu_list:
        price = float(cpu[3]); benchmark = int(cpu[2])
        if price <= MAX_D and benchmark > max_cpu_benchmark:
            max_cpu_benchmark = benchmark; best_cpu = cpu
    return best_cpu, max_cpu_benchmark

# find the best cpu for Intel and AND
best_intel, max_intel_bench = best(intel); best_amd, max_amd_bench=best(amd)


# lists to hold data about the graphs
intel_g1 =[]; amd_g1=[]; intel_g2=[]; amd_g2=[]

def insert_data(cpu_list, new_list, mode):
    """Function to insert data to the list based on the chosen mode

    Keyword arguments:

    cpu_list -- takes an list of either the Intel or AMD CPUs
    new_list -- list to append the data to
    mode -- benchmark/cost or benchmark vs cost
    """

    for data in cpu_list:
        # extract the cost and benchmark from Intel or AMD cpu list
        cost = float(data[3]); benchmark = int(data[2])

        if mode == "benchmark_divide_cost":
            new_list.append([benchmark / cost, benchmark])

        elif mode == "benchmark_vs_cost":
            new_list.append([cost, benchmark])


# perfomance vs performance/$
insert_data(intel, intel_g1, "benchmark_divide_cost" )
intel_bench_cost, intel_benchmarks = zip(*intel_g1)

insert_data(amd, amd_g1, "benchmark_divide_cost")
amd_bench_cost, amd_bench = zip(*amd_g1)


# performance vs cost
insert_data(intel, intel_g2, "benchmark_vs_cost")
intel_cost, intel_benchmark = zip(*intel_g2)

insert_data(amd, amd_g2, "benchmark_vs_cost")
amd_cost, amd_benchmark = zip(*amd_g2)


def scatter(d1, d2, color, marker, label, zorder):
    """Function to plot the scatter plot

    Keyword Arguments:

    d1 -- dataset1
    d2 -- dataset2
    color -- color of the markers
    marker -- the marker
    label -- the label
    zorder -- the zorder
    """

    plt.scatter(d1, d2, color=color, marker=marker, label=label, zorder=zorder)


def annotate(best_type, plt_x_coord, plt_y_coord, txt_x_coord, txt_y_coord):
    """Function to annotate the graphs

    Keyword Arguments:

    best_type -- the best type of CPU
    plt_x_coord -- the x coordinate the point is at
    plt_y_coord -- the y coordinate the point is at
    txt_x_coord -- the x coordinate the text is at
    txt_y_coord -- the y coordinate the text is at
    """
    plt.annotate(
        f"{best_type[0]} ${int(float(best_type[3]))}",
        xy=(plt_x_coord, plt_y_coord),
        xytext=(txt_x_coord, txt_y_coord),
        arrowprops=dict(arrowstyle='->', color="#7e7f80", linestyle='dotted'),
        fontsize=10, color='black', zorder=0
    )


# Performance vs Performance / $
plt.figure(figsize=(14, 6))

plt.subplot(121);
plot = plt.gca()
plot.locator_params(axis='x', nbins=9, min_n_ticks=9)
plot.locator_params(axis='y', nbins=10, min_n_ticks=10)
plt.axis([0, 200, 1000, 100000]);
plt.grid(True, axis="y");

plt.xlabel('cpuMark / $'); plt.ylabel('cpuMark');
plt.title('Performance vs. Performance / $');

scatter(intel_bench_cost, intel_benchmarks, "blue", "$In$", "Intel", 0)
scatter(amd_bench_cost,amd_bench,"red","$A$","AMD",1);
plt.legend()

annotate(best_amd,  round(int(best_amd[2]) / float(best_amd[3])),
int(best_amd[2]), 30, 95000)

annotate(best_intel, round(int(best_intel[2]) / float(best_intel[3])),
 int(best_intel[2]), 70, 82000)


# Performance vs Cost
plt.subplot(122); plt.xscale('log')
plt.xticks([35, 50, 100, 250, 500, 1000, 2500, 5000],
           ["35", "50", "100", "250", "500", "1000", "2500", "5000"])
plt.locator_params(axis='y', nbins=10, min_n_ticks=10)
plt.axis([40, 10000, 1000, 100000]); plt.subplots_adjust(wspace=0.175)

plt.xlabel('Price in USD');
plt.ylabel('cpuMark')
plt.title('Performance vs. Cost');
plt.grid(True, axis="y")

scatter(intel_cost, intel_benchmark, "blue", "$In$", "Intel", 0)
scatter(amd_cost, amd_benchmark, "red", "$A$", "AMD", 1)

annotate(best_intel, float(best_intel[3]), int(best_intel[2]), 55, 75000)
annotate(best_amd, float(best_amd[3]), int(best_amd[2]), 55, 95000)

plt.suptitle(f"Best CPU Under ${MAX_D}", y=0.96, fontsize=16);
plt.show()



