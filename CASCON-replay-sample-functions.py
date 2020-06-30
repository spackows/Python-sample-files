

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


def plotWordCloud( results_list, WordCloud, plt ):
    actions_str  = ""
    keywords_str = ""
    for result in results_list:
        if( len(result["actions"]) > 0 ):
            actions_str += ' '.join(result["actions"]) + " "
        if( len(result["keywords"]) > 0 ):
            keywords_str += ' '.join(result["keywords"]) + " "
    wordcloud_actions = WordCloud().generate( actions_str )
    wordcloud_keywords = WordCloud().generate( keywords_str )
    fig, axs = plt.subplots( 1, 2, figsize=( 20, 10 ) )
    axs[0].imshow( wordcloud_actions )
    axs[0].set_title( "Actions", fontsize=20 )
    axs[0].axis( "off" )
    axs[1].imshow( wordcloud_actions )
    axs[1].set_title( "Keywords", fontsize=20 )
    axs[1].axis( "off" )



