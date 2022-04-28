import shutil

import matplotlib.pyplot as plt
import numpy as np

import website.models.db as db


def aggregator_dict_sum_chart(attribute, dict, iter_item):
    """ Generate dictionary counter"""
    if iter_item[attribute] in dict:
        dict[iter_item[attribute]] += 1
    else:
        dict[iter_item[attribute]] = 1


def plot_creator(data_dict, title, lab_y=''):
    """ Generate custom bar charts
        data_dict = data_dictionary - must be a dictionary
        title = name of the chart
        lab_y = label y; default empty
    """
    x_ls, y_ls = list(data_dict.keys()), list(data_dict.values())

    change_flag = False
    # Prevent exaggerated size
    if len(x_ls) == 1:
        change_flag = True
        x_ls.append('')
        y_ls.append(0)

    plt.bar(x_ls, y_ls, width=0.5)
    plt.ylabel(lab_y)
    plt.yticks(np.arange(0, max(y_ls) + 1, step=1))

    if change_flag:
        x_ls.pop()
    for each_value in range(len(x_ls)):
        plt.text(x=each_value, y=y_ls[each_value], s=y_ls[each_value], ha="center")

    plt.title(title)
    plt.savefig('website/static/images/' + title + '.png')
    plt.close()


def generate_charts():
    """ Generate charts"""
    data = db.retrieve_all()
    # Will move these to a function once development is confirmed.
    # Reference to matplotlib docs
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

    counts_chart(data)
    apps_chart(data)
    skills_chart(data)


def chart_collection_defence(data, target, chart_names):
    """ In the event of a missing collection, chart creation will not be compromised entirely."""
    try:
        return [chart.to_dict() for chart in data[target]]
    except KeyError:
        # No chart can be created if at least one "application" collection does not exist.
        # This defends against the page crash error.
        source = "website/static/images/inf-load-free.gif"

        for each_chart in chart_names:
            destin = 'website/static/images/' + each_chart + '.png'
            shutil.copyfile(source, destin)
        return False


def counts_chart(data):
    """ Counts chart - count.png
        Data consists of Applications, Skills, and Contacts entries on record
    """
    data_records_count = [len(data["applications"]), len(data["skills"]), len(data["contacts"])]

    plt.bar(['Applications', 'Skills', 'Contacts'], data_records_count)
    plt.ylabel('Count')
    plt.yticks(np.arange(0, max(data_records_count) + 1, step=1))

    for each_value in range(len(data_records_count)):
        plt.text(x=each_value, y=data_records_count[each_value], s=data_records_count[each_value], ha="center")

    plt.title('Entries Recorded')
    plt.savefig('website/static/images/count.png')
    plt.close()


def apps_chart(data):
    """ Generate app data
    """
    chart_names = [
        "Positions Applied",
        "Application Statuses",
        "Position Types",
        "Companies Applied"
    ]
    app_in_depth = chart_collection_defence(data, "applications", chart_names)

    if not app_in_depth:
        return

    positions, dates, types, status, companies = {}, {}, {}, {}, {}
    for each_app in app_in_depth:
        aggregator_dict_sum_chart("position", positions, each_app)
        aggregator_dict_sum_chart("type", types, each_app)
        aggregator_dict_sum_chart("date", dates, each_app)
        aggregator_dict_sum_chart("status", status, each_app)
        aggregator_dict_sum_chart("company", companies, each_app)

    # Due to names are locally managed
    plot_creator(positions, chart_names[0])
    plot_creator(status, chart_names[1])
    plot_creator(types, chart_names[2])
    plot_creator(companies, chart_names[3])


def apps_active_data_chart(data):
    pass


def skills_chart(data):
    """ Skills charts """
    chart_names = [
        "Your Skills"
    ]
    skill_in_depth = chart_collection_defence(data, "skills", chart_names)

    if not skill_in_depth:
        return

    skills_freq_count = {}
    for each_skill in skill_in_depth:
        aggregator_dict_sum_chart("skill", skills_freq_count, each_skill)

    plot_creator(skills_freq_count, chart_names[0])


def global_skills(data):
    """ All data per users - moniker 'How do you compare?'"""
    pass
