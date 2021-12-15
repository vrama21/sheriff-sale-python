import { ActionType, Listing } from 'types';

export interface Action {
  counties?: string[];
  currentPage?: number;
  listing?: Listing;
  listings?: Listing[];
  saleDates?: string[];
  type: ActionType;
}
