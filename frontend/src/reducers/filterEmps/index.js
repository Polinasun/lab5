import * as types from './actionTypes';

const initialState = {
    filters: {}
}

export default (state = initialState, action) => {
    switch(action.type) {
        case types.FILTER_EMPS: {
            return {...state, filters: action.payload}
        }
        default: return state;
    }
    
}