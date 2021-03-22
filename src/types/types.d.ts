
export type Filter = {
  county: string,
  city: string,
  saleDate: string,
}

export type ButtonEvent = React.ChangeEvent<HTMLButtonElement>

export type ListingInterface = {
  id: number,
  address?: string,
  address_sanitized?: string,
  attorney?: string,
  attorney_phone?: string,
  city?: string,
  county?: string,
  court_case?: string,
  deed?: string,
  deed_address?: string,
  defendant?: string,
  description?: string,
  judgment?: string,
  maps_url?: string,
  parcel?: string,
  plaintiff?: string,
  priors?: string,
  sale_date?: string,
  secondary_unit?: string,
  sheriff?: string,
  status_history?: Record<string, unknown>,
  unit?: string,
  unit_secondary?: string,
  upset_amount?: number,
  zip_code?: string,
};