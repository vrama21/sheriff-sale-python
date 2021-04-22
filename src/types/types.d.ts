export interface Filter {
  county: string;
  city: string;
  saleDate: string;
}

export type ButtonEvent = React.ChangeEvent<HTMLButtonElement>;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Dispatch = { (value: any): void; (arg0: { type: string; listings?: Record<string, unknown>[] }): void };

export interface SearchFiltersProps {
  counties: string[];
  citiesByCounty: Record<string, Record<'cities', string[]>>;
  filters: Filter;
  onFilterChange: (
    event: React.ChangeEvent<{
      name?: string;
      value: unknown;
    }>,
    child: React.ReactNode,
  ) => void;
  onFilterReset: (event: React.FormEvent<Element>) => void;
  onFilterSubmit: (event: React.FormEvent<Element>) => void;
  saleDates: string[];
}

export interface ListingInterface {
  id: number;
  address: string;
  attorney?: string;
  attorney_phone?: string;
  city?: string;
  county: string;
  court_case?: string;
  created_on?: Date,
  deed?: string;
  deed_address?: string;
  defendant?: string;
  description?: string;
  judgment?: number;
  latitude?: string | float;
  longitude?: string | float;
  maps_url?: string;
  parcel?: string;
  plaintiff?: string;
  priors?: string;
  sale_date: string;
  secondary_unit?: string;
  sheriff_id?: string;
  state: string;
  status_history?: Record<string, unknown>;
  street?: string;
  unit?: string;
  unit_secondary?: string;
  upset_amount?: number;
  zip_code?: string;
}

export interface URLParams {
  listingId: string;
}
