
export interface EnumeratedArrayOfObjects {
  [index: number]: { [key: string]: Object[] }
}

export interface useFetchInterface {
  [key: string]: Object[]
}

export interface Filter {
  county: string,
  city: string,
  saleDate: string,
}

export type ButtonEvent = React.ChangeEvent<HTMLButtonElement>

export type Listing = {
  address: string,
  address_sanitized: string,
  attorney: string,
  city: string,
  county: string,
  court_case: string,
  defendant: string,
  id: number,
  judgment: string,
  maps_url?: string,
  plaintiff: string,
  priors: string,
  sale_date: string,
  secondary_unit?: string,
  sheriff: string,
  unit?: string,
  zip_code: string,
};