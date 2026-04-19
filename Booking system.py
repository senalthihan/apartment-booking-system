# ProgFunA2_s4099547.py
# Name: Senal
# Student ID: s4099547
# Highest level attempted: Level 4

import sys
import csv
import datetime
import os

class DateInputError(Exception):
    pass

class QuantityError(Exception):
    pass

class RedemptionError(Exception):
    pass

class NotFoundError(Exception):
    pass

class InvalidGuestError(Exception):
    pass

class InvalidProductError(Exception):
    pass

class InvalidDateError(Exception):
    pass


class Guest:
    """
    Stores guest identity and reward details.
    reward_rate (%): for example, 100 means 1 point per $1
    redeem_rate (%): for example, 1 means each point is $0.01
    """
    def __init__(self, guest_id, name, reward_points):
        self._id = str(guest_id)
        self._name = name
        self._reward_rate = 100.0
        self._redeem_rate = 1.0
        self._reward_points = int(round(float(reward_points)))

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_reward_rate(self):
        return self._reward_rate

    def get_redeem_rate(self):
        return self._redeem_rate

    def get_reward_balance(self):
        return self._reward_points

    def set_reward_rate(self, new_rate_percent):
        self._reward_rate = float(new_rate_percent)

    def set_redeem_rate(self, new_rate_percent):
        self._redeem_rate = float(new_rate_percent)

    def update_reward(self, delta_points):
        self._reward_points += int(delta_points)

    def calc_earned_points(self, total_cost):
        pts = round(float(total_cost) * (self._reward_rate / 100.0))
        return int(pts)

    def display_info(self):
        print('ID:', self._id, 'Name:', self._name,
              'Reward rate(%):', self._reward_rate,
              'Redeem rate(%):', self._redeem_rate,
              'Points:', self._reward_points)


class Product:
    """Base class for all orderable things."""
    def __init__(self, prod_id, name, price):
        self._id = str(prod_id)
        self._name = name
        self._price = float(price)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def display_info(self):
        print('ID:', self._id, 'Name:', self._name, 'Price:', self._price)


class ApartmentUnit(Product):
    """Apartment product with capacity (beds)."""
    def __init__(self, prod_id, name, price, capacity):
        Product.__init__(self, prod_id, name, price)
        self._capacity = int(capacity)

    def get_capacity(self):
        return self._capacity

    def display_info(self):
        print('ID:', self.get_id(), 'Name:', self.get_name(),
              'Rate per night:', self.get_price(), 'Capacity:', self._capacity)


class SupplementaryItem(Product):
    """Add-on product (for example breakfast, car park)."""
    def display_info(self):
        print('ID:', self.get_id(), 'Name:', self.get_name(),
              'Unit price:', self.get_price())


class Bundle(Product):
    """Product made of multiple other products."""
    def __init__(self, bundle_id, name, price, product_list=None):
        Product.__init__(self, bundle_id, name, price)
        if product_list is None:
            self._product_list = []
        else:
            self._product_list = list(product_list)

    def add_product(self, product):
        if product not in self._product_list:
            self._product_list.append(product)

    def get_products(self):
        return self._product_list

    def display_info(self):
        print('Bundle ID:', self.get_id(),
              'Name:', self.get_name(),
              'Price:', self.get_price())
        if len(self._product_list) == 0:
            print('Includes: (none)')
        else:
            print('Includes:')
            for p in self._product_list:
                if hasattr(p, 'get_name'):
                    print('-', p.get_name())
                else:
                    print('-', str(p))


class Order:
    """
    Represents a complete booking with multiple products.
    Stores all items, dates, and booking timestamp.
    """
    def __init__(self, guest_obj, booking_datetime):
        self._guest = guest_obj
        self._booking_datetime = booking_datetime  # datetime object
        self._items = []  # list of (product, quantity, checkin_str, checkout_str)
        self._total_cost = 0.0
        self._discount = 0.0
        self._final_cost = 0.0
        self._earned_points = 0
        self._num_guests = 0

    def set_num_guests(self, n):
        self._num_guests = n

    def get_num_guests(self):
        return self._num_guests

    def add_item(self, product, quantity, checkin_str=None, checkout_str=None):
        self._items.append((product, quantity, checkin_str, checkout_str))

    def get_items(self):
        return self._items

    def get_guest(self):
        return self._guest

    def get_booking_datetime(self):
        return self._booking_datetime

    def set_costs(self, total, discount, final, earned):
        self._total_cost = total
        self._discount = discount
        self._final_cost = final
        self._earned_points = earned

    def get_total_cost(self):
        return self._total_cost

    def get_discount(self):
        return self._discount

    def get_final_cost(self):
        return self._final_cost

    def get_earned_points(self):
        return self._earned_points


class Records:
    """Central data repository with guests, products, orders."""
    def __init__(self):
        self.guests = []
        self.products = []
        self.orders = []

    def add_guest(self, guest_obj):
        self.guests.append(guest_obj)

    def add_product(self, product_obj):
        self.products.append(product_obj)

    def add_order(self, order_obj):
        self.orders.append(order_obj)

    def list_guests(self):
        for g in self.guests:
            g.display_info()

    def list_products(self):
        for p in self.products:
            p.display_info()

    def add_bundle(self, bundle_obj):
        self.products.append(bundle_obj)

    def list_bundles(self):
        any_found = False
        for p in self.products:
            if isinstance(p, Bundle):
                p.display_info()
                any_found = True
        if not any_found:
            print('No bundles found.')

    def find_guest_by_id(self, gid):
        for g in self.guests:
            if g.get_id() == gid:
                return g
        return None

    def find_product_by_id(self, pid):
        for p in self.products:
            if p.get_id() == pid:
                return p
        return None

    def list_orders(self):
        for o in self.orders:
            g = o.get_guest()
            items = o.get_items()
            print('Guest:', g.get_name(), '| Items:', len(items), '| Final cost: $', '{:.2f}'.format(o.get_final_cost()))

    def compute_guest_spend(self):
        """Returns dict {guest_id: total_spend}."""
        spend = {}
        for o in self.orders:
            g = o.get_guest()
            spend[g.get_id()] = spend.get(g.get_id(), 0.0) + o.get_final_cost()
        return spend

    def compute_product_sales(self):
        """Returns dict {product_id: (qty_sold, revenue)}."""
        sales = {}
        for o in self.orders:
            for prod, qty, ci, co in o.get_items():
                if prod.get_id() not in sales:
                    sales[prod.get_id()] = [0, 0.0]
                sales[prod.get_id()][0] += qty
                sales[prod.get_id()][1] += prod.get_price() * qty
        return sales



class Operations:
    def __init__(self):
        self.rec = Records()
        self._seed_sample_data()

    def _seed_sample_data(self):
        self.rec.add_guest(Guest('G001', 'Alyssa', 200))
        self.rec.add_guest(Guest('G002', 'Luigi', 320))
        self.rec.add_product(ApartmentUnit('U12swan', 'U12swan', 95.0, 2))
        self.rec.add_product(ApartmentUnit('U209duck', 'U209duck', 106.7, 3))
        self.rec.add_product(ApartmentUnit('U49goose', 'U49goose', 145.2, 4))
        self.rec.add_product(SupplementaryItem('car_park', 'car_park', 25.0))
        self.rec.add_product(SupplementaryItem('breakfast', 'breakfast', 21.0))
        self.rec.add_product(SupplementaryItem('toothpaste', 'toothpaste', 5.0))
        b1 = Bundle('B001', 'Swan + Breakfast Pack', 130.0, product_list=['U12swan', 'breakfast'])
        self.rec.add_bundle(b1)

    def load_files(self, guests_path=None, products_path=None, orders_path=None):
        if guests_path:
            self._load_guests_csv(guests_path)
        if products_path:
            self._load_products_csv(products_path)
        if not self.rec.guests and not self.rec.products:
            self._seed_sample_data()
        if orders_path:
            self._load_orders_csv(orders_path)

    def _load_guests_csv(self, path):
        try:
            with open(path, 'r', encoding='utf-8-sig', newline='') as f:
                rdr = csv.reader(f)
                self.rec.guests.clear()
                for row in rdr:
                    if not row or len(row) < 3:
                        continue
                    gid = str(row[0]).strip()
                    name = row[1].strip()
                    reward_rate = 100.0
                    redeem_rate = 1.0
                    reward_points = 0
                    if len(row) >= 3:
                        try:
                            reward_points = int(float(row[2]))
                        except:
                            reward_points = 0
                    if len(row) >= 4:
                        try:
                            reward_rate = float(row[3])
                        except:
                            reward_rate = 100.0
                    if len(row) >= 5:
                        try:
                            redeem_rate = float(row[4])
                        except:
                            redeem_rate = 1.0
                    g = Guest(gid, name, reward_points)
                    g.set_reward_rate(reward_rate)
                    g.set_redeem_rate(redeem_rate)
                    self.rec.add_guest(g)
            print('Loaded guests from', path)
        except Exception as e:
            print('Failed to load guests from', path, '-', e)

    def _load_products_csv(self, path):
   
   
        def _is_float(s):
            try:
                float(s); return True
            except:
                return False

        def _split_includes(cell):
            raw = (cell or "").strip()
            if not raw:
                return []
        # accept  + or whitespace as separators
            for sep in ['|', ';', ',', '+']:
                raw = raw.replace(sep, ' ')
            return [p.strip() for p in raw.split() if p.strip()]

        try:
            with open(path, 'r', encoding='utf-8-sig', newline='') as f:
                rdr = csv.reader(f)
                self.rec.products.clear()

                apts_loaded = items_loaded = bundles_loaded = 0

                for row in rdr:
                    if not row: 
                        continue
                # strip except empties
                    row = [ (c or '').strip() for c in row ]
                    if len(row) == 0:
                        continue

                # skip  header
                    if row[0].lower() in ('id', 'product_id', '#', 'code'):
                        continue

                    pid = row[0]

                # -Bundle detection 
                    if pid.upper().startswith('B') and len(row) >= 3:
                        name = row[1]

                    # many columns, last is numeric price
                        if len(row) >= 4 and _is_float(row[-1]) and len(row) > 4:
                            price = float(row[-1])
                            included = [c for c in row[2:-1] if c]
                    #  4 columns, the 3rd is delimited list, 4th is price
                        elif len(row) == 4 and _is_float(row[3]):
                            price = float(row[3])
                            included = _split_includes(row[2])
                        else:
                        # last cell numeric, middle cells are IDs
                            if _is_float(row[-1]) and len(row) > 3:
                                price = float(row[-1])
                                included = [c for c in row[2:-1] if c]
                            else:
                                continue 

                        self.rec.add_bundle(Bundle(pid, name, price, product_list=included))
                        bundles_loaded += 1
                        continue

                #  Apartment: id,name,price,capacity 
                    if len(row) >= 4 and _is_float(row[2]):
                        name = row[1]
                        price = float(row[2])
                        try:
                            capacity = int(float(row[3]))
                            self.rec.add_product(ApartmentUnit(pid, name, price, capacity))
                            apts_loaded += 1
                            continue
                        except:
                            pass  # fall through to item parsing

                # Supplementary item: id,name,price 
                    if len(row) >= 3 and _is_float(row[2]):
                        name = row[1]
                        price = float(row[2])
                        self.rec.add_product(SupplementaryItem(pid, name, price))
                        items_loaded += 1
                        continue

                print(f'Loaded products from {path} '
                      f'({apts_loaded} apartments, {items_loaded} items, {bundles_loaded} bundles)')
        except Exception as e:
            print('Failed to load products from', path, '-', e)


    def _load_orders_csv(self, path):
        """
        Load orders in format:
        guest_id, qty x prod_id, qty x prod_id, ..., total_cost, earned_pts, date_time
        """
        try:
            with open(path, 'r', encoding='utf-8-sig', newline='') as f:
                rdr = csv.reader(f)
                loaded = 0
                for row in rdr:
                    if not row or len(row) < 4:
                        continue

                    gid = row[0].strip()
                    guest = self._find_guest_by_id(gid)
                    if guest is None:
                        print('Warning: guest not found:', gid)
                        continue
                    
                    # Parse booking datetime (second to last column)
                    booking_str = row[-1].strip()
                    try:
                        booking_dt = datetime.datetime.strptime(booking_str, '%d/%m/%Y %H:%M')
                    except:
                        booking_dt = datetime.datetime.now()
                    
                    order = Order(guest, booking_dt)
                    
                    # Parse items (from index 1 to -3)
                    for i in range(1, len(row) - 2):
                        item_str = row[i].strip()
                        if ' x ' not in item_str:
                            continue
                        parts = item_str.split(' x ')
                        if len(parts) != 2:
                            continue
                        qty_str = parts[0].strip()
                        pid = parts[1].strip()
                        if not qty_str.isdigit():
                            continue
                        qty = int(qty_str)
                        prod = self._find_product_by_id(pid)
                        if prod is None:
                            continue
                        order.add_item(prod, qty, None, None)
                    
                    # Parse total cost and earned points
                    try:
                        total_cost = float(row[-2])
                        earned_pts = int(float(row[-3])) if len(row) >= 4 else 0
                    except:
                        total_cost = 0.0
                        earned_pts = 0
                    
                    order.set_costs(total_cost, 0.0, total_cost, earned_pts)
                    guest.update_reward(earned_pts)
                    self.rec.add_order(order)
                    loaded += 1
            print('Loaded', loaded, 'orders from', path)
        except FileNotFoundError:
            print('Orders file not found:', path, '(continuing).')
        except Exception as e:
            print('Cannot load the order file:', e)


    def save_files(self, guests_path=None, products_path=None, orders_path=None):
        if guests_path:
            self._save_guests_csv(guests_path)
        if products_path:
            self._save_products_csv(products_path)
        if orders_path:
            self._save_orders_csv(orders_path)

    def _save_guests_csv(self, path):
        try:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                for g in self.rec.guests:
                    w.writerow([g.get_id(), g.get_name(),
                                g.get_reward_balance(),
                                '{:.2f}'.format(g.get_reward_rate()),
                                '{:.2f}'.format(g.get_redeem_rate())])
            print('Saved guests to', path)
        except Exception as e:
            print('Failed to save guests:', e)

    def _save_products_csv(self, path):
        try:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                for p in self.rec.products:
                    if isinstance(p, ApartmentUnit):
                        w.writerow([p.get_id(), p.get_name(),
                                    '{:.2f}'.format(p.get_price()),
                                    p.get_capacity()])
                    elif isinstance(p, SupplementaryItem):
                        w.writerow([p.get_id(), p.get_name(),
                                    '{:.2f}'.format(p.get_price())])
                    elif isinstance(p, Bundle):
                        row = [p.get_id(), p.get_name()]
                        row.extend(p.get_products())
                        row.append('{:.2f}'.format(p.get_price()))
                        w.writerow(row)
                    else:
                        w.writerow([p.get_id(), p.get_name(),
                                    '{:.2f}'.format(p.get_price())])
            print('Saved products to', path)
        except Exception as e:
            print('Failed to save products:', e)

    def _save_orders_csv(self, path):
        """
        Save in format:
        guest_id, qty x prod_id, qty x prod_id, ..., earned_pts, total_cost, date_time
        """
        try:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                for o in self.rec.orders:
                    row = [o.get_guest().get_id()]
                    for prod, qty, ci, co in o.get_items():
                        row.append(str(qty) + ' x ' + prod.get_id())
                    row.append('{:.2f}'.format(o.get_final_cost()))
                    row.append(str(o.get_earned_points()))
                    row.append(o.get_booking_datetime().strftime('%d/%m/%Y %H:%M'))
                    w.writerow(row)
            print('Saved orders to', path)
        except Exception as e:
            print('Failed to save orders:', e)

    def show_orders(self):
        print('\n-- Orders --')
        self.rec.list_orders()

    def show_guest_history(self):
        print('\nDisplay a guest order history')
        name = input('Enter guest name: ').strip()
        if not name.replace(' ', '').isalpha():
            print('Invalid name.')
            return
        guest = None
        for g in self.rec.guests:
            if g.get_name().lower() == name.lower():
                guest = g
                break
        if guest is None:
            print('Guest not found.')
            return
        guest_orders = [o for o in self.rec.orders if o.get_guest() is guest]
        print('\nThis is the booking and order history for', name + '.')
        if not guest_orders:
            print('No order history found for', name)
            return
        print('Order ID | Products Ordered | Total Cost | Earned Rewards')
        for i, o in enumerate(guest_orders, 1):
            items_str = ', '.join([str(qty) + ' x ' + prod.get_name() for prod, qty, ci, co in o.get_items()])
            print('Order' + str(i), '|', items_str, '| $' + '{:.2f}'.format(o.get_final_cost()), '|', o.get_earned_points())

    def show_stats_and_export(self):
        spend = self.rec.compute_guest_spend()
        sales = self.rec.compute_product_sales()
        gid_to_name = {g.get_id(): g.get_name() for g in self.rec.guests}
        pid_to_name = {p.get_id(): p.get_name() for p in self.rec.products}
        top_guests = sorted(spend.items(), key=lambda x: x[1], reverse=True)[:3]
        top_products = sorted(sales.items(), key=lambda x: x[1][0], reverse=True)[:3]
        try:
            with open('stats.txt', 'w', encoding='utf-8') as f:
                f.write('Top 3 most valuable guests (by spending)\n')
                for i, (gid, dollars) in enumerate(top_guests, 1):
                    f.write(f'{i} {gid_to_name.get(gid, gid)} ${dollars:,.2f}\n')
                f.write('\nTop 3 products (by quantities sold)\n')
                for i, (pid, (qty, rev)) in enumerate(top_products, 1):
                    f.write(f'{i} {pid_to_name.get(pid, pid)} {qty} ${rev:,.2f}\n')
            print('Wrote stats to stats.txt')
        except Exception as e:
            print('Failed to write stats.txt:', e)
        print('\n-- Stats preview --')
        print('Top guests:')
        for i, (gid, dollars) in enumerate(top_guests, 1):
            print(i, gid_to_name.get(gid, gid), '${:,.2f}'.format(dollars))
        print('Top products:')
        for i, (pid, (qty, rev)) in enumerate(top_products, 1):
            print(i, pid_to_name.get(pid, pid), qty, '${:,.2f}'.format(rev))

    def _find_guest_by_id(self, gid):
        for g in self.rec.guests:
            if g.get_id() == gid:
                return g
        return None

    def _find_product_by_id(self, pid):
        for p in self.rec.products:
            if p.get_id() == pid:
                return p
        return None

    def _calc_nights(self, checkin_str, checkout_str):
        try:
            d1 = datetime.datetime.strptime(checkin_str.strip(), '%d/%m/%Y').date()
            d2 = datetime.datetime.strptime(checkout_str.strip(), '%d/%m/%Y').date()
        except Exception:
            raise InvalidDateError('Invalid date format. Please use d/m/yyyy.')
        if d2 <= d1:
            raise InvalidDateError('Check-out must be after check-in.')
        return (d2 - d1).days

    def _input_int(self, prompt, min_val=None, max_val=None):
        while True:
            s = input(prompt).strip()
            try:
                val = int(s)
            except ValueError:
                raise QuantityError('Please enter a valid integer.')
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                raise QuantityError('Number out of valid range.')
            return val

    def _input_float(self, prompt, min_val=None):
        while True:
            s = input(prompt).strip()
            try:
                v = float(s)
            except ValueError:
                print('Please enter a valid number.')
                continue
            if min_val is not None and v < min_val:
                print('Enter a number >=', min_val)
                continue
            return v

    def show_guests(self):
        print('\n-- Guests --')
        if not self.rec.guests:
            print('No guests found.')
            return
        for g in self.rec.guests:
            g.display_info()

    def show_products(self):
        print('\n-- Products --')
        if not self.rec.products:
            print('No products found.')
            return
        for p in self.rec.products:
            p.display_info()

    def show_bundles(self):
        print('\n-- Bundles --')
        any_found = False
        for p in self.rec.products:
            if isinstance(p, Bundle):
                p.display_info()
                any_found = True
        if not any_found:
            print('No bundles found.')

    def add_update_apartment(self):
        print('\nAdd/Update ApartmentUnit')
        apt_id = input('Apartment ID (e.g., U12swan): ').strip()
        name = apt_id
        rate = self._input_float('Rate per night: $', min_val=0.01)
        cap = self._input_int('Capacity (beds): ', min_val=1)
        existing = self._find_product_by_id(apt_id)
        if existing and isinstance(existing, ApartmentUnit):
            self.rec.products.remove(existing)
        self.rec.add_product(ApartmentUnit(apt_id, name, rate, cap))
        print('Saved apartment', apt_id)

    def add_update_supplementary(self):
        print('\nAdd/Update SupplementaryItem')
        item_id = input('Item ID (e.g., breakfast): ').strip()
        name = item_id
        price = self._input_float('Unit price: $', min_val=0.01)
        existing = self._find_product_by_id(item_id)
        if existing and isinstance(existing, SupplementaryItem):
            self.rec.products.remove(existing)
        self.rec.add_product(SupplementaryItem(item_id, name, price))
        print('Saved item', item_id)

    def add_update_bundle(self):
        print('\nAdd/Update Bundle')
        b_id = input('Bundle ID (e.g., B001): ').strip()
        b_name = input('Bundle name: ').strip()
        b_price = self._input_float('Bundle price: $', min_val=0.01)
        raw = input('Included product IDs (comma-separated, e.g., U12swan, breakfast): ').strip()
        ids = [x.strip() for x in raw.split(',') if x.strip() != '']
        missing = [pid for pid in ids if self._find_product_by_id(pid) is None]
        if missing:
            print('These product IDs do not exist:', ', '.join(missing))
            print('Bundle not saved.')
            return
        existing = self._find_product_by_id(b_id)
        if existing and isinstance(existing, Bundle):
            self.rec.products.remove(existing)
        b = Bundle(b_id, b_name, b_price, product_list=ids)
        self.rec.add_bundle(b)
        print('Saved bundle', b_id)

    def update_all_reward_rate(self):
        print('\nUpdate Reward Rate for ALL guests')
        new_rate = self._input_float('Enter new reward rate % (e.g., 100 for 1 point per $1): ', min_val=0.0)
        for g in self.rec.guests:
            g.set_reward_rate(new_rate)
        print('Updated reward rate for', len(self.rec.guests), 'guests.')

    def update_all_redeem_rate(self):
        print('\nUpdate Redeem Rate for ALL guests')
        while True:
            new_rate = self._input_float('Enter new redeem rate % (e.g., 1 for $0.01 per point): ', min_val=0.0)
            if new_rate < 1.0:
                print('Too low to be worth claiming. Must be >= 1%.')
                continue
            break
        for g in self.rec.guests:
            g.set_redeem_rate(new_rate)
        print('Updated redeem rate for', len(self.rec.guests), 'guests.')

    def make_order_multi(self):
        print('\n-- Make an order (multi-item) --')
        print('Available guests (ID : Name):')
        for g in self.rec.guests:
            print(g.get_id(), ':', g.get_name())
        
        # Guest validation with exception handling
        while True:
            try:
                gid = input('Enter guest ID or name: ').strip()
                if not gid.replace(' ', '').isalpha() and not gid.startswith('G'):
                    raise InvalidGuestError('Invalid guest input.')
                guest = self._find_guest_by_id(gid)
                if guest is None:
                    for g in self.rec.guests:
                        if g.get_name().lower() == gid.lower():
                            guest = g
                            break
                if guest is None:
                    yn = input('Guest not found. Create new guest? (y/n): ').strip().lower()
                    if yn == 'y':
                        while True:
                            new_name = input('Enter guest name (alphabet only): ').strip()
                            if not new_name.replace(' ', '').isalpha():
                                print('Name must contain only alphabet characters.')
                                continue
                            break
                        new_gid = 'G' + str(len(self.rec.guests) + 1).zfill(3)
                        guest = Guest(new_gid, new_name, 0)
                        self.rec.add_guest(guest)
                        print('Created new guest:', new_name, '(ID:', new_gid + ')')
                    else:
                        return
                break
            except InvalidGuestError as e:
                print(str(e), 'Please try again.')

        # Number of guests
        while True:
            try:
                num_guests = self._input_int('Number of guests: ', min_val=1)
                break
            except QuantityError as e:
                print(str(e), 'Please try again.')

        # Cart items
        cart = []
        apartment_item = None
        checkin_date = None
        checkout_date = None
        
        while True:
            print('\nAvailable items (ID : Name : Price : Type)')
            for p in self.rec.products:
                if isinstance(p, Bundle):
                    label = 'Bundle'
                elif isinstance(p, ApartmentUnit):
                    label = 'Apartment'
                else:
                    label = 'Item'
                print(p.get_id(), ':', p.get_name(), ': $', '{:.2f}'.format(p.get_price()), ':', label)

            pid = input('\nEnter product/bundle ID to add (or blank to finish): ').strip()
            if pid == '':
                break

            try:
                prod = self._find_product_by_id(pid)
                if prod is None:
                    raise InvalidProductError('Product not found.')

                if isinstance(prod, ApartmentUnit):
                    if apartment_item is not None:
                        print('Only one apartment per order allowed.')
                        continue
                    print('Apartment booking requires dates.')
                    while True:
                        try:
                            ci = input('Check-in (d/m/yyyy): ').strip()
                            co = input('Check-out (d/m/yyyy): ').strip()
                            nights = self._calc_nights(ci, co)
                            if nights <= 0:
                                raise InvalidDateError('Stay length must be positive.')
                            checkin_date = ci
                            checkout_date = co
                            qty = nights
                            apartment_item = (prod, qty, ci, co)
                            cart.append((prod, qty, ci, co))
                            print('Added', prod.get_name(), 'for', qty, 'night(s).')
                            break
                        except InvalidDateError as e:
                            print(str(e), 'Please try again.')
                else:
                    while True:
                        try:
                            qty = self._input_int('Enter quantity: ', min_val=1)
                            cart.append((prod, qty, None, None))
                            print('Added to cart.')
                            break
                        except QuantityError as e:
                            print(str(e), 'Please try again.')


            except InvalidProductError as e:
                print(str(e), 'Please try again.')

        if len(cart) == 0:
            print('No items selected.')
            return

        
        # Validate apartment or bundle is present
        has_bundle = any(isinstance(p, Bundle) for p, _, _, _ in cart)
        if apartment_item is None and not has_bundle:
            print('Every order must contain an apartment reservation or a bundle.')
            return


        # Calculate original total
        original_total = 0.0
        for prod, qty, ci, co in cart:
            original_total += prod.get_price() * qty

        # Points redemption
        print('\nCurrent reward balance for', guest.get_name(), ':', guest.get_reward_balance(), 'points')
        max_redeem_dollars = original_total
        redeem_rate_dollar_per_point = guest.get_redeem_rate() / 100.0
        if redeem_rate_dollar_per_point <= 0:
            points_cap_by_total = 0
        else:
            points_cap_by_total = int(max_redeem_dollars / redeem_rate_dollar_per_point)

        allowed_points = min(guest.get_reward_balance(), points_cap_by_total)
        
        if guest.get_reward_balance() >= 100:
            print('You may redeem up to', allowed_points, 'points this purchase.')
            while True:
                try:
                    redeem_pts = self._input_int('Redeem how many points? (0-' + str(allowed_points) + '): ', min_val=0, max_val=allowed_points)
                    break
                except QuantityError:
                    print('Invalid input. Try again.')
        else:
            redeem_pts = 0
            print('Need at least 100 points to redeem.')

        # Compute costs
        discount_dollars = redeem_pts * redeem_rate_dollar_per_point
        final_total = original_total - discount_dollars
        if final_total < 0:
            final_total = 0.0

        earned_pts = guest.calc_earned_points(final_total)

        # Update guest points
        if redeem_pts > 0:
            guest.update_reward(-redeem_pts)
        if earned_pts > 0:
            guest.update_reward(earned_pts)

        # Create order with booking timestamp
        booking_datetime = datetime.datetime.now()
        order = Order(guest, booking_datetime)
        order.set_num_guests(num_guests)
        for prod, qty, ci, co in cart:
            order.add_item(prod, qty, ci, co)
        order.set_costs(original_total, discount_dollars, final_total, earned_pts)
        self.rec.add_order(order)

        
        # Print receipt
        print('\n' + '='*65)
        print('Guest name:', guest.get_name())
        print('Number of guests:', num_guests)

        if apartment_item:
            apt_prod, apt_qty, apt_ci, apt_co = apartment_item
            print('Apartment name:', apt_prod.get_name())
            print('Apartment rate: $' + '{:.2f}'.format(apt_prod.get_price()), '(AUD)')
            print('Check-in date:', apt_ci)
            print('Check-out date:', apt_co)
            print('Length of stay:', apt_qty, '(nights)')
            print('Booking date:', booking_datetime.strftime('%d/%m/%Y %H:%M'))
            apt_subtotal = apt_prod.get_price() * apt_qty
            print('Sub-total: $' + '{:.2f}'.format(apt_subtotal), '(AUD)')
        else:
            print('(No standalone apartment selected — bundle-only booking)')


        
        # Supplementary items
        print('-'*65)
        print('Additional items (incl. bundles)')
        print('ID\tName\t\tQuantity\tUnit Price $\tCost')

        supp_subtotal = 0.0
        for prod, qty, ci, co in cart:
            if not isinstance(prod, ApartmentUnit):
                line_cost = prod.get_price() * qty
                supp_subtotal += line_cost
                print(
                    prod.get_id(), '\t',
                    (prod.get_name()[:15]).ljust(15), '\t',
                    qty, '\t\t',
                    '{:.2f}'.format(prod.get_price()), '\t\t',
                    '{:.2f}'.format(line_cost)
                )


        print('Sub-total: $' + '{:.2f}'.format(supp_subtotal))
        print('-'*65)
        print('Total cost: $' + '{:.2f}'.format(original_total), '(AUD)')
        print('Reward points to redeem:', redeem_pts, '(points)')
        print('Discount based on points: $' + '{:.2f}'.format(discount_dollars), '(AUD)')
        print('Final total cost: $' + '{:.2f}'.format(final_total), '(AUD)')
        print('Earned rewards:', earned_pts, '(points)')
        print('Thank you for your booking!')
        print('We hope you will have an enjoyable stay.')
        print('='*65)



    def run(self, guests_path=None, products_path=None, orders_path=None):
        while True:
            print('\n==== A2 Level 4 Menu ====')
            print('1. Display guests')
            print('2. Display products')
            print('3. Display bundles')
            print('4. Display orders')
            print('5. Add/Update ApartmentUnit')
            print('6. Add/Update SupplementaryItem')
            print('7. Add/Update Bundle')
            print('8. Update ALL guests reward rate (%)')
            print('9. Update ALL guests redeem rate (%)')
            print('10. Make an order (multi-item)')
            print('11. Guest order history')
            print('12. Generate & export statistics')
            print('13. Save files now')
            print('14. Exit (save)')
            choice = input('Choose (1-14): ').strip()

            if choice == '1':
                self.show_guests()
            elif choice == '2':
                self.show_products()
            elif choice == '3':
                self.show_bundles()
            elif choice == '4':
                self.show_orders()
            elif choice == '5':
                self.add_update_apartment()
            elif choice == '6':
                self.add_update_supplementary()
            elif choice == '7':
                self.add_update_bundle()
            elif choice == '8':
                self.update_all_reward_rate()
            elif choice == '9':
                self.update_all_redeem_rate()
            elif choice == '10':
                self.make_order_multi()
            elif choice == '11':
                self.show_guest_history()
            elif choice == '12':
                self.show_stats_and_export()
            elif choice == '13':
                self.save_files(guests_path, products_path, orders_path)
            elif choice == '14':
                self.save_files(guests_path, products_path, orders_path)
                print('Goodbye!')
                break
            else:
                print('Invalid option.')


def _parse_args(argv):
    """
    Supports:
      -g <guests.csv>
      -p <products.csv>
      -o <orders.csv>
    All optional.
    """
    guests_path = None
    products_path = None
    orders_path = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == '-g' and i + 1 < len(argv):
            guests_path = argv[i + 1]
            i += 2
        elif arg == '-p' and i + 1 < len(argv):
            products_path = argv[i + 1]
            i += 2
        elif arg == '-o' and i + 1 < len(argv):
            orders_path = argv[i + 1]
            i += 2
        else:
            i += 1
    return guests_path, products_path, orders_path



if __name__ == '__main__':
    g_path, p_path, o_path = _parse_args(sys.argv[1:])

    # Default to local filenames if nothing was passed
    if not (g_path or p_path or o_path):
        g_path, p_path, o_path = 'guests.csv', 'products.csv', 'orders.csv'

    #  absolute relative to .py file
    base = os.path.dirname(os.path.abspath(__file__))
    g_path = os.path.join(base, g_path) if g_path else None
    p_path = os.path.join(base, p_path) if p_path else None
    o_path = os.path.join(base, o_path) if o_path else None

    app = Operations()
    app.load_files(g_path, p_path, o_path)
    app.run(g_path, p_path, o_path)
