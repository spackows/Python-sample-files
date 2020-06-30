from collections import OrderedDict
import random
from matplotlib import colors as mcolors
import numpy as np


def analyzeSampleMessages( questions_problems_text, nlu, Features, KeywordsOptions, SemanticRolesOptions ):
    results_list = []
    for message in questions_problems_text:
        result = nlu.analyze( text=message, features=Features( keywords=KeywordsOptions(), semantic_roles=SemanticRolesOptions() ) ).get_result()
        actions_arr = []
        keywords_arr = []
        for keyword in result["keywords"]:
            keywords_arr.append( keyword["text"] )
        if( "semantic_roles" in result ):
            for semantic_result in result["semantic_roles"]:
                if( "action" in semantic_result ):
                    actions_arr.append( semantic_result["action"]["normalized"] )
        results_list.append( { "header"   : "-------------------------------------------------------------",
                               "message"  : message,
                               "actions"  : actions_arr,
                               "keywords" : keywords_arr,
                               "spacer"   : "" } )
    return results_list;


def plotWordCloud( results_list, WordCloud, plt, STOPWORDS ):
    actions_str  = ""
    keywords_str = ""
    for result in results_list:
        if( len(result["actions"]) > 0 ):
            actions_str += ' '.join(result["actions"]) + " "
        if( len(result["keywords"]) > 0 ):
            keywords_str += ' '.join(result["keywords"]) + " "
    my_stopwords = { "try", "keep", "use", "want", "need", "know", "give", "help", "tell", "might", "cant", "say", "cause" "place" }
    
    wordcloud_actions = WordCloud( stopwords=STOPWORDS.union( my_stopwords ) ).generate( actions_str )
    wordcloud_keywords = WordCloud().generate( keywords_str )
    fig, axs = plt.subplots( 1, 2, figsize=( 20, 10 ) )
    axs[0].imshow( wordcloud_actions )
    axs[0].set_title( "Actions", fontsize=20 )
    axs[0].axis( "off" )
    axs[1].imshow( wordcloud_actions )
    axs[1].set_title( "Keywords", fontsize=20 )
    axs[1].axis( "off" )
    plt.show()


def countWords( results_list, entity_type, minimum ):
    all_words = {}
    for result in results_list:
        words_arr = result[entity_type]
        for word in words_arr:
            if( word not in all_words ):
                all_words[word] = 0
            all_words[word] += 1
    common_words = dict( [ (k,v) for k,v in all_words.items() if v > minimum ] )
    ordered_common_words = OrderedDict( sorted( common_words.items(), key=lambda x:x[1], reverse=True ) )
    return ordered_common_words


def random_colours( num ):
    rand_indexes = random.sample(range(0, len( mcolors.CSS4_COLORS.keys() ) - 1 ), num )
    colour_list = [ list( mcolors.CSS4_COLORS.keys() )[i] for i in rand_indexes ]
    return colour_list


def plotDefaultCharts( results_list ):
    actions = countWords( results_list, "actions",  3 )
    actions_labels = list( actions.keys() )[0:6]
    actions_values = list( actions.values() )[0:6]
    actions_positions = np.arange( 6 )
    actions_colours = random_colours( 6 )
    keywords = countWords( results_list, "keywords", 3 )
    keywords_labels = list( keywords.keys() )[0:6]
    keywords_values = list( keywords.values() )[0:6]
    keywords_positions = np.arange( 6 )
    keywords_colours = random_colours( 6 )
    fig, axs = plt.subplots( 2, 1, figsize=( 8, 5 ) )
    axs[0].bar( actions_positions,   actions_values,   color=actions_colours,   edgecolor="black" )
    axs[0].set_title( 'Actions',  fontsize=20 )
    plt.sca(axs[0])
    plt.xticks( actions_positions, actions_labels,   fontsize=13 )
    axs[1].bar( actions_positions,   actions_values,   color=actions_colours,   edgecolor="black" )
    axs[1].set_title( 'Keywords',  fontsize=20 )
    plt.sca(axs[1])
    plt.xticks( keywords_positions, keywords_labels,   fontsize=13 )
    fig.tight_layout()
    plt.show()


