import matplotlib.pyplot as plt
import numpy as np

import website.models.db as db


FOLDER = 'website/static/images/analytics/'


def generate_charts(req_data):
    """ Generate charts"""
    data = db.retrieve_all()
    # Reference to matplotlib docs
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

    counts_chart(data, req_data['charts'], req_data['userID'])
    apps_chart(data, req_data['charts'], req_data['userID'])
    skills_chart(data, req_data['charts'], req_data['userID'])


def aggregator_dict_sum_chart(attribute, dict, iter_item):
    """ Generate dictionary counter"""
    if iter_item[attribute] in dict:
        dict[iter_item[attribute]] += 1
    else:
        dict[iter_item[attribute]] = 1


def plot_no_data(title):
    """ Generate an empty chart with the text "No Data" on center."""
    plt.bar([], [])

    plt.text(x=0, y=0,
             s='No Data\nTry adding in some information before returning to this page!',
             ha='center',
             va='center',
             bbox=dict(
                boxstyle="square",
                facecolor="white"
                ))

    plt.yticks([])
    plt.xticks([])

    plt.title(title)
    plt.savefig(FOLDER + title + '.png')
    plt.close()


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

    plt.bar(x_ls, y_ls)
    plt.ylabel(lab_y)
    plt.yticks(np.arange(0, max(y_ls) + 1, step=1))

    if change_flag:
        x_ls.pop()
    for each_value in range(len(x_ls)):
        plt.text(x=each_value, y=y_ls[each_value], s=y_ls[each_value], ha="center")

    plt.title(title)
    plt.savefig(FOLDER + title + '.png')
    plt.close()


def plot_creator_horizontal(data_dict, title, lab_y=''):
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

    plt.barh(x_ls, y_ls)
    plt.ylabel(lab_y)
    plt.yticks([])
    plt.xticks(np.arange(0, max(y_ls) + 1, step=1))

    if change_flag:
        x_ls.pop()
    for each_value in range(len(x_ls)):
        plt.text(
            y=each_value,
            x=y_ls[each_value],
            s=x_ls[each_value],
            ha="center",
            bbox=dict(
                boxstyle="square",
                facecolor="white"
            )
        )

    plt.title(title)
    plt.savefig(FOLDER + title + '.png')
    plt.close()


def chart_collection_defence(data, target, chart_names):
    """ In the event of a missing collection, chart creation will not be compromised entirely."""
    try:
        export_dat_list = [chart.to_dict() for chart in data[target]]
        if len(export_dat_list) == 0:
            faux = data['error123']  # noqa: F841
        return export_dat_list
    except KeyError:
        # No chart can be created if at least one "application" collection does not exist.
        # This defends against the page crash error.

        for each_chart in chart_names:
            plot_no_data(each_chart)
        return False


def empty_charts_by_names(chart_names):
    """ Create empty charts based on the supplied named list"""
    for each_chart in chart_names:
        plot_no_data(each_chart)


def chart_data_verification(data, collection, chart_names, user_id):
    """ Verifies the data to generate charts.
        Returns the data by user id or False if data fails the check.
    """
    # empty check
    data_in_depth = chart_collection_defence(data, collection, chart_names)
    if not data_in_depth:
        empty_charts_by_names(chart_names)
        return False

    user_dat = [dat for dat in data_in_depth if dat["userID"] == user_id]

    # Force a list from the destructure
    if isinstance(user_dat, str):
        user_dat = [user_dat]

    if isinstance(chart_names, str):
        chart_names = [chart_names]

    if len(user_dat) == 0:
        empty_charts_by_names(chart_names)
        return False

    return user_dat


def user_chart_counter(data, collection, user_id):
    """ Count data created by the specific user id."""
    summation = 0
    for each_data in data[collection]:
        if each_data.to_dict()["userID"] == user_id:
            summation += 1
    return summation


def counts_chart(data, chart_names, user_id):
    """ Counts chart - count.png
        Data consists of Applications, Skills, and Contacts entries on record
    """
    title = chart_names[0]
    data_records_count = [
        user_chart_counter(data, "applications", user_id),
        user_chart_counter(data, "skills", user_id),
        user_chart_counter(data, "contacts", user_id),
    ]

    if max(data_records_count) == 0:
        plot_no_data(title)
        return

    plt.bar(['Applications', 'Skills', 'Contacts'], data_records_count)
    plt.ylabel('Count')
    plt.yticks(np.arange(0, max(data_records_count) + 1, step=1))

    for each_value in range(len(data_records_count)):
        plt.text(x=each_value, y=data_records_count[each_value], s=data_records_count[each_value], ha="center")

    plt.title(title)
    plt.savefig(FOLDER + title + '.png')
    plt.close()


def apps_chart(data, chart_titles, user_id):
    """ Generate app data
    """
    chart_names = chart_titles[1:5]

    user_app = chart_data_verification(data, "applications", chart_names, user_id)
    if user_app is False:
        return

    positions, dates, types, status, companies = {}, {}, {}, {}, {}
    for each_app in user_app:
        aggregator_dict_sum_chart("position", positions, each_app)
        aggregator_dict_sum_chart("type", types, each_app)
        aggregator_dict_sum_chart("date", dates, each_app)
        aggregator_dict_sum_chart("status", status, each_app)
        aggregator_dict_sum_chart("company", companies, each_app)

    # Due to names are locally managed
    plot_creator_horizontal(positions, chart_names[0])
    plot_creator_horizontal(status, chart_names[1])
    plot_creator_horizontal(types, chart_names[2])
    plot_creator_horizontal(companies, chart_names[3])
    plot_date_line(dates, chart_titles[6])


def plot_date_line(data_dict, title):
    x_ls, y_ls = list(data_dict.keys()), list(data_dict.values())

    plt.plot_date(x_ls, y_ls, linestyle='solid')
    plt.ylabel("Job Entries Tracked")
    plt.yticks(np.arange(0, max(y_ls) + 1, step=1))

    plt.title(title)
    plt.savefig(FOLDER + title + '.png')
    plt.close()


def skills_chart(data, chart_names, user_id):
    """ Skills charts """
    chart_names = chart_names[5]

    user_skill = chart_data_verification(data, "skills", chart_names, user_id)
    if user_skill is False:
        return

    skills_freq_count = {}
    for each_skill in user_skill:
        aggregator_dict_sum_chart("skill", skills_freq_count, each_skill)

    plot_creator_horizontal(skills_freq_count, chart_names)


def global_companies(data):
    """ All data per users - moniker 'How do you compare?'"""
    pass
