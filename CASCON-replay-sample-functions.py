

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




