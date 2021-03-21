
export type Filter = {
  county: String,
  city: String,
  saleDate: String,
}

export type ButtonEvent = React.ChangeEvent<HTMLButtonElement>

export type ListingInterface = {
  id: Number,
  address?: String,
  address_sanitized?: String,
  attorney?: String,
  attorney_phone?: String,
  city?: String,
  county?: String,
  court_case?: String,
  deed?: String,
  deed_address?: String,
  defendant?: String,
  description?: String,
  judgment?: String,
  maps_url?: String,
  parcel?: String,
  plaintiff?: String,
  priors?: String,
  sale_date?: String,
  secondary_unit?: String,
  sheriff?: String,
  status_history?: Object[] | null,
  unit?: String,
  unit_secondary?: String,
  upset_amount?: Number,
  zip_code?: String,
};