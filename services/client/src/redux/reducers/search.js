export function searchTerm(state="",action) {
    switch (action.type) {
        case 'SEARCH_TERM_MODIFIED':
            return action.text;  
        default:
            return state;
    }
}