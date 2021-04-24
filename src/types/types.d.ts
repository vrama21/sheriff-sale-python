export { Filter, SearchFiltersProps } from 'components/SearchFilters/SearchFilters';
export { ListingInterface } from 'components/Listing/Listing';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Dispatch = { (value: any): void; (arg0: { type: string; listings?: Record<string, unknown>[] }): void };

export interface URLParams {
  listingId: string;
}
